from django.urls import path, re_path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    path('', BlogHome.as_view(), name='home'),
    path('about/', about, name='about'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('contact/', ContactViewForm.as_view(), name='contact'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='show_post'),
    path('category/<slug:category_slug>/', cache_page(60)(BlogCategory.as_view()), name='category'),
    # path('categories/<int:catid>', categories),
    # path('about/', about, name='about'),
    # re_path(r'^archive/(?P<year>[0-9]{4})/', archive),
]