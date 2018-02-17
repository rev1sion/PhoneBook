from django.shortcuts import render
from django.views.generic import ListView, DetailView

from back.profiles.models import User, PhoneNumber
from back.companies.models import Office
# Create your views here.


class UserListView(ListView):
    model = User
    paginate_by = 8

    def get_queryset(self):
        return User.objects.filter(is_active=True)


class UserDetailView(DetailView):
    model = User





