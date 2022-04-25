from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from .models import *
from .utils import *



class BlogHome(DataMixin, ListView):
    # paginate_by = 3
    model = Blog
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    # extra_context = {
    #     'title': 'Главная страница'
    # }
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['menu'] = menu
        # context['title'] = 'Главная страница'
        # context['category_selected'] = 0
        c_def = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(c_def.items()))

    def qet_queryset(self):
        return Blog.objects.filter(is_published=True).select_related('category')

# def index(request):
#     posts = Blog.objects.all()
#
#
#     context ={
#         'posts': posts,
#         'menu': menu,
#         'title': 'Главная страница',
#         'category_selected': 0,
#     }
#     return render(request, 'blog/index.html', context=context)

def about(request):
    contact_list = Blog.objects.all()
    paginator = Paginator(contact_list, 3)

    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)

    context = {
        'menu': menu,
        'page_obj': page_obj,
        'title': 'О сайте'
    }

    return render(request, 'blog/about.html', context=context)

class ShowPost(DataMixin,DetailView):
    model = Blog
    template_name = 'blog/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(c_def.items()))

# def show_post(request, post_slug):
#     # return HttpResponse(f"Отображение статьи с id = {post_id}")
#     posts = get_object_or_404(Blog, slug=post_slug)
#     context = {
#         'menu': menu,
#         'post': posts,
#         'title': posts.title,
#         'category_selected': posts.category
#     }
#     return render(request, 'blog/post.html', context=context)

class BlogCategory(DataMixin, ListView):
    model = Blog
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Blog.objects.filter(category__slug=self.kwargs['category_slug'], is_published=True).select_related('category')


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['category_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                                      category_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))

# def show_category(request, category_id):
#     posts = Blog.objects.filter(category_id=category_id)
#
#     if len(posts) == 0:
#         raise Http404()
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Категории',
#         'category_selected': category_id,
#     }
#     return render(request, 'blog/index.html', context=context)

# def contact(request):
#     context = {
#         'menu': menu,
#         'title': 'Контакты'
#     }
#     return render(request, 'blog/contact.html', context=context)


class ContactViewForm(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'blog/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self,* ,object_list=None ,**kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')

class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'blog/add_page.html'
    # login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')
        return dict(list(context.items()) + list(c_def.items()))

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'blog/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self,*,object_list=None ,**kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'blog/login.html'

    def get_context_data(self,*,object_list=None ,**kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    # def get_success_url(self):
    #     return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('login')
# def add_page(request):
#     # if int(year) > 2020:
#     #     return redirect('home', permanent=True)
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             try:
#                 # Blog.objects.create(**form.cleaned_data)
#                 form.save()
#                 return redirect('home')
#             except:
#                 form.add_error(None, 'ОшибОчка')
#     else:
#         form = AddPostForm()
#
#     context = {
#         'menu': menu,
#         'title': 'Добавить статью',
#         'form': form,
#     }
#     return render(request, 'blog/add_page.html', context=context)

def pageNotFound(request, exception):
    return HttpResponseNotFound(f"<h1>Нет страницы =(</h1>")


