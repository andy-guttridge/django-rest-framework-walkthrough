from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):
    def setUp(self):
        # Create a dummy user for our tests
        User.objects.create_user(username='andy', password='12345')

    def test_can_list_posts(self):
        """
        Test we can list posts
        """
        # Get a reference to the test user and create
        # a post using their permissions.
        user = User.objects.get(username='andy')
        Post.objects.create(owner=user)
        # Make a get request for the post list
        response = self.client.get('/posts/')
        # Test if the expected HTTP status code is returned
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
    
    def test_logged_in_user_can_create_post(self):
        # Log our dummy user in.
        self.client.login(username='andy', password='12345')
        # Make a post request with data
        response = self.client.post('/posts/', {'title': 'a title'})
        # Count how many posts and check if there is only one as expected
        count = Post.objects.count()
        self.assertEqual(count, 1)
        # Check the HTTP response code is 201 for a created record
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_logged_in_user_cannot_create_post(self):
        # Make sure our user is logged out
        self.client.logout()
        # Make a post request with data
        response = self.client.post('/posts/', {'title': 'a title'})
        # Count how many posts and check there are none as expected
        count = Post.objects.count()
        self.assertEqual(count, 0)
        # Check the HTTP response code is 403 forbidden
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)