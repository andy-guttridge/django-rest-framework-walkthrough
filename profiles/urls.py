from django.urls import path
from profiles import views

urlpatterns = [
    path('profiles/', views.ProfileList.as_view()),
    # This is the url for our detail view which allows us to retrieve
    # a single profile by its primary key in the URL.
    path('profiles/<int:pk>/', views.ProfileDetail.as_view()),
]
