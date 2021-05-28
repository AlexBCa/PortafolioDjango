from django import forms
from .models import Post, Category, Comment

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        # Son los campos que va ha interactuar el formulario, por ello active no esta aquí. 
        fields = ('author','body')