from django.test import TestCase
from app.models import Blog
# Create your tests here.

class TestModel(TestCase):


    def test_get_blog(self):
        blog = Blog.getBlogById(1)
        print(blog.id)
        print(blog.title)
        self.assertEqual(True, True)


