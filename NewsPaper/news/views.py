from datetime import datetime
from django.shortcuts import render

from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from .filters import PostFilter
from .forms import PostForm
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Post, Category
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin


class PostList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'posts'
    ordering = ['-dateCreation']
    paginate_by = 3

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())

    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            "filter": self.get_filter(),
        }
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())

        context['posts'] = Post.objects.all()
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса

        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не ошибся, то сохраняем новый товар
            form.save()

        return super().get(request, *args, **kwargs)

    def __str__(self):
        return f'{self.author}: {self.postTitle}'


class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'

    queryset = Post.objects.all()

class SearchList(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'
    ordering = ['-dateCreation']
    paginate_by = 30

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            "filter": self.get_filter(),
        }


class PostCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'sample_app/post_create.html'
    form_class = PostForm
    permission_required = ('news.add_post',)
    success_url = '/news/'


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'sample_app/post_create.html'
    form_class = PostForm
    permission_required = ('news.change_post',)
    success_url = '/news/'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'sample_app/post_delete.html'
    queryset = Post.objects.all()
    permission_required = ('news.delete_post',)
    success_url = '/news/'
