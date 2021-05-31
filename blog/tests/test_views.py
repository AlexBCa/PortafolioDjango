from django.contrib.auth.models import AnonymousUser
from blog.models import Category, Post
from django.test import Client
from django.test import TestCase, RequestFactory
from blog.views import BlogCategory, BlogDetailView, BlogInterestFromView
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

        self.blog_index_url = reverse('blog_index')
        self.blog_category_url = reverse('blog_category', args=['Django'])
        self.blog_detail_view_url = reverse('blog_detail', args=[1])
        self.blog_BlogInterestFromView_url = reverse('blog_detail', args=[1])
        self.blog_viewStaff_url = reverse('staff')
        self.blog_viewPrivate_url = reverse('private')

        
        # Creamos una entrada en el blog 
        self.post = Post.posts.create(
            title='Entrada test',
            body='Prueba test',
            created_on = date.today(),
            last_modified = date.today(),

        )


    
    def test_blog_index_get(self):
        response = self.client.get(self.blog_index_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog_index.html')

    def test_blog_category_get(self):
        response = self.client.get(self.blog_category_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog_category.html')

    

    def test_blog_category_get_queryset(self):
        
        # Enviamos una solicitud GET a la url de category
        request = self.factory.get(self.blog_category_url )
        
       
        view_category = BlogCategory()
        
        # Los parametros kwards se deben pasar como parametros unicos, no como dicionarios.
        view_category.setup(request, category='Django')


        # Guardamos el queryset
        queryset = view_category.get_queryset()

        queryset_control = Post.posts.filter(
            # Utilizamos la varaible category para filtrar la categoria enviada.
            categories__name__contains='Django'

        ).order_by('-created_on')

        self.assertQuerysetEqual(queryset, queryset_control)

      
    def test_blogDetailView_get(self):
        response = self.client.get(self.blog_detail_view_url)

        self.assertEqual(response.status_code, 200)

    def test_blogDetailView_context_data(self):
        
        response = self.client.get(self.blog_detail_view_url)
        self.assertIsNotNone(response.context['form'])
        self.assertIsNotNone(response.context['comments'])

    def test_BlogInterestFromView_get(self):

        response = self.client.get(self.blog_BlogInterestFromView_url)
        self.assertEqual(response.status_code, 200)



    def test_BlogInterestFormView_POST(self):

        
        params = {
            'author': 'Alex', 
            'body': 'test'
        }

        self.user = User.objects.create_user(
            username='alex')

        self.client.force_login(self.user)

        response = self.client.post(self.blog_BlogInterestFromView_url, params)


        self.assertEqual(response.status_code, 302)

    
    def test_blogView_set_get(self):
        response = self.client.get(self.blog_detail_view_url)

        self.assertIsNotNone(response.context['view'])
        self.assertEquals(type(response.context['view']), type(BlogDetailView()) )


    def test_blogView_set_post(self):

        params = {
            'author': 'Alex', 
            'body': 'test'
        }

        self.user = User.objects.create_user(
            username='alex')

        self.client.force_login(self.user)
        response = self.client.post(self.blog_BlogInterestFromView_url)

        self.assertIsNotNone(response.context['view'])
        self.assertEquals(type(response.context['view']), type(BlogInterestFromView()) )
        

    def test_ViewStaff_is_staff(self):
        
        # Iniciamos como superusuario.
        self.user = User.objects.create_superuser('myuser', 'myemail@test.com', 'mypassword')
        
        self.client.force_login(self.user)

        response = self.client.get(self.blog_viewStaff_url)
        
        self.assertEqual(response.status_code, 200)


    def test_ViewStaff_not_staff(self):
        
        
        self.user = User.objects.create_user('myuser')
        
        self.client.force_login(self.user)

        response = self.client.get(self.blog_viewStaff_url)
        
        self.assertEqual(response.status_code, 302)
    
    def test_privada_is_login(self):
        
        
        self.user = User.objects.create_user('myuser', 'myemail@test.com', 'mypassword')
        
        self.client.force_login(self.user)

        response = self.client.get(self.blog_viewPrivate_url)
        
        self.assertEqual(response.status_code, 200)

    def test_privada_not_login(self):

        response = self.client.get(self.blog_viewPrivate_url)
        
        self.assertEqual(response.status_code, 302)







