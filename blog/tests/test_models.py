from django.test import TestCase
from blog.models import Category, Post, Comment
from datetime import date

class TestModels(TestCase):

    def setUp(self):
        
        self.category = Category.objects.create(name='Pasteles')
        self.post = Post.posts.create(
            title='Entrada test',
            body='Prueba test',
            created_on = date.today(),
            last_modified = date.today(),
            


        )
        # se relaciona el post con la categoria Pasteles
        self.post.categories.add(self.category)

        self.comment = Comment.objects.create(
            author = 'Testing 1',
            body = 'Testenado',
            created_on = date.today(),
            post = self.post
        )


    
    def test_Category_creation(self):

        self.assertEqual(self.category.__str__(), 'Pasteles')
    
    def test_post_creation(self):

        self.assertEqual(self.post.__str__(), 'Entrada test')

    def test_comments_creation(self):

        self.assertEqual(self.comment.__str__(), 'Testing 1')
