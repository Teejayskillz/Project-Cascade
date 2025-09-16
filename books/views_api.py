from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
import json 

from books.models import ReadingProgress

@login_required
@require_GET
def story_progress(request, story_id):
    """return the last read chapter and scroll position for a story"""
    prog = ReadingProgress.objects.filter(user=request.user, story_id=story_id).first()
    if prog:
        return JsonResponse({
            "chapter_id": prog.last_read_chapter.id,
            "scroll": prog.scroll_position,
            "char": prog.char_position,
        })
    return JsonResponse({"chapter_id": None, "scroll": 0, "char": 0})

@login_required
@require_POST
def save_story_progress(request, story_id):
    """save the last read chapter and scroll position for a story"""
    data = json.loads(request.body)
    ReadingProgress.objects.update_or_create(
        user=request.user,
        story_id=story_id,
        defaults={
            "last_read_chapter_id": data.get("chapter_id"),
            "scroll_position": data.get("scroll", 0),
            "char_position": data.get("char", 0),       
        }
    )
    return JsonResponse({"status": "success"})