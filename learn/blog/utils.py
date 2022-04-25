from django.core.cache import cache
from django.db.models import Count

from .models import *

menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Контакты', 'url_name': 'contact'},
        {'title': 'Добавить статью', 'url_name': 'add_page'},
        # {'title': 'Войти в аккаунт', 'url_name': 'login'}
]

class DataMixin:
    paginate_by = 3
    def get_user_context(self, **kwargs):
        context = kwargs
        categories = Category.objects.all()
        # categories = cache.get('categories')
        if not categories:
            categories = Category.objects.annotate(Count('blog'))
            cache.set('categories', categories)

        # categories = Category.objects.annotate(Count('blog'))
        # context['menu'] = menu
        user_menu = menu.copy()

        if not self.request.user.is_authenticated:
            user_menu.pop(2)

        context['menu'] = user_menu
        context['categories'] = categories
        if 'category_selected' not in context:
            context['category_selected'] = 0
        return context