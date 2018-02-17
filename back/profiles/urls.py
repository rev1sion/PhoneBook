from django.urls import path, include
from back.profiles import views


urlpatterns = [
    path('', views.UserListView.as_view(), name='user-list'),
    path('<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
]