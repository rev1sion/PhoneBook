from django.shortcuts import render
from django.views.generic import ListView, DetailView
# Create your views here.


def home(request):
    context = {
        'user': request.user,
    }

    return render(request, 'index.html', context, locals())


# def ProfileListView(ListView):
#     model = profile
#     paginate_by = 8
#
#
# def ProfileDetailView(DetailView):
#     model = profile

