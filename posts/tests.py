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


class PostDetailViewTests(APITestCase):
    def setUp(self):
        # Create two users and a post for each user for our tests
        user1 = User.objects.create_user(username='andy', password='12345')
        user2 = User.objects.create_user(username='lindsay', password='12345')
        Post.objects.create(
            owner=user1, title='Post Title', content='Andys content'
        )
        Post.objects.create(
            owner=user2, title='Post Title 2', content='Lindsays content'
        )

    def test_can_retrieve_post_using_valid_id(self):
        # Make a get request  for the first post
        response = self.client.get('/posts/1/')
        # Test if the post title is as expected
        self.assertEqual(response.data['title'], 'Post Title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_not_retrieve_post_by_invalid_post_id(self):
        # Make a get request for a non-existent post
        response = self.client.get('/posts/999/')
        # Test that the response is the expected 404 error
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_post(self):
        # Login and make a PUT request to change the title of one of our test
        # posts
        self.client.login(username="andy", password="12345")
        response = self.client.put('/posts/1/', {'title': 'Test Post'})
        post = Post.objects.filter(pk=1).first()
        # Test post title is as expected and HTTP 200 code returned
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_update_another_users_post(self):
        # Login and make a request to change the title of a post made by
        # another user
        self.client.login(username="andy", password="12345")
        response = self.client.put('/posts/2/', {'title': 'New Post Title'})
        # Test HTTP 403 code is returned
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
