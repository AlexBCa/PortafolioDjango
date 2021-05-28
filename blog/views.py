from django.db.models.base import Model
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import generic
from .models import Category, Post, Comment
from .forms import CommentForm
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
# Create your views here.

# Vista encargada de mostrar todo los post ordenados por orden de creación descendente.
class BlogIndex(generic.ListView):


    queryset = Post.posts.all().order_by('-created_on')
    template_name = 'blog_index.html'

# Vista encargada de mostrar los post por su categoria.
class BlogCategory(generic.ListView):

    template_name = 'blog_category.html'

   


    # llamamos a get_queryset para sobreescribir queryset y agregarle más logica.
    def get_queryset(self):

        # Obtiene un parametro pasado por un GET
        category = self.kwargs['category']
    
        
        return Post.posts.filter(
            # Utilizamos la varaible category para filtrar la categoria enviada.
            categories__name__contains=category

        ).order_by('-created_on')

    

# Vista encargada de mostrar cada pagina del post y sus comentarios
# es decir, responde cuando se le envia un GET.
class BlogDetailView(generic.DetailView):
    model = Post
    template_name = 'blog_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        # Obtenemos del objeto post actual los objetos commentarios relacionados.

        context['comments'] = self.object.relation.all()
        return context

# Vista encargada de agregar un comentario, al responder a un POST
class BlogInterestFromView(generic.detail.SingleObjectMixin, generic.FormView):
    template_name = 'blog_detail.html'
    form_class = CommentForm
    model = Post

    def post(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog_detail', kwargs={'pk': self.object.pk})


    def form_valid(self, form):

        
        new_comment = form.save(commit=False)
        # Asignamos la relación del nuevo comentario con el post actual.
        new_comment.post = self.object
        
        new_comment.save()
        


        return super().form_valid(form)

# Lanza una vista o otra dependiendo de si la solicitud es un GET o un POST.
class BlogView(generic.View):

    def get(self, request, *args, **kwargs):
        view = BlogDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = BlogInterestFromView.as_view()
        return view(request, *args, **kwargs)

# Nos permite ver la pagina solo si estamos registrados. 
# Los mixin simpre deben ir primero.
class ViewPrivada(LoginRequiredMixin, generic.TemplateView):
    # Pagina de login
    login_url = '/users/'
    # Texto que aparece en la redireción de la url.
    redirect_field_name = 'redirect_to'

    template_name = 'private_page.html'

# Creamos una vista que solo pueden acceder los usuarios con permiso de staff.
class ViewStaff(LoginRequiredMixin, UserPassesTestMixin, generic.TemplateView):

    template_name = 'staff_page.html'
    login_url = '/users/'
   
    # Hacemos que el test sea si es staff
    def test_func(self):
        return self.request.user.is_staff

    # Si no tiene permiso lo redirecionamos a la pagina de login.
    def handle_no_permission(self):
        return redirect('/users/')

    

