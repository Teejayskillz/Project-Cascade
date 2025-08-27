from django.core.paginator import Paginator
from django.shortcuts import render
from books.models import Story

def home(request):
    # get all stories ordered by latest
    story_list = Story.objects.all().order_by('-published_date')
    
    # paginate - 9 per page
    paginator = Paginator(story_list, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/home.html', {
        'stories': page_obj,                 # so {% for story in stories %} works
        'page_obj': page_obj,                # for pagination controls
        'is_paginated': page_obj.has_other_pages(),
        'paginator': paginator
    })
