from django.shortcuts import render
from django.db.models import Q
from books.models import Story
from users.models import CustomUser  

# Create your views here.

def search_view(request):
    q = request.GET.get('q', '')
    stories = []
    users = []
    if q:
        stories = Story.objects.filter(
            Q(title__icontains=q) | Q(synopsis__icontains=q)
        )
        users = CustomUser.objects.filter(
            Q(username__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q)
        )

    return render(request, 'search/search_results.html', {
        'query': q,
        'stories': stories,
        'users': users
    })