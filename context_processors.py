# mblogapp/context_processors.py

from .models import Category

def categories(request):
    categories = Category.objects.all()
    return {'categories': categories}
