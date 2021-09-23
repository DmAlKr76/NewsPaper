from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
from .models import Post, Category, Author
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required

class PostsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-id')
    paginate_by = 10

    def get_query_data(self, **kwargs):
        query = super().get_context_data(**kwargs)
        query['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        context['is_not_authorized'] = not self.request.user.is_authenticated
        return context


class PostSearch(ListView):
    model = Post
    template_name = 'news_search.html'
    context_object_name = 'news_search'
    ordering = ['-Post_time']
    paginate_by = 10

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context['filter'] = PostFilter(self.request.GET,
#                        queryset=self.get_queryset())
#        return context

    def get_context_data(self, *args, **kwargs):
        return {
        **super().get_context_data(*args, **kwargs),
        "filter": self.get_filter(),
        }

    def get_index_data(self, **kwargs):
        index = super().get_context_data(**kwargs)
        index['is_not_authorized'] = not self.request.user.groups.filter(name='common').exists()
        return index


class PostDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'news_.html'
    context_object_name = 'news_'
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        context['is_not_authorized'] = not self.request.user.groups.filter(name='common').exists()
        return context

class PostAdd(PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'news_add.html'
    form_class = PostForm
    permission_required = ('news.add_post',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='author').exists()
        context['is_not_authorized'] = not self.request.user.is_authenticated
        return context

class PostEdit(PermissionRequiredMixin, UpdateView):
    template_name = 'news_edit.html'
    form_class = PostForm
    permission_required = ('news.change_post',)

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='author').exists()
        return context

    def get_index_data(self, **kwargs):
        index = super().get_context_data(**kwargs)
        index['is_not_authorized'] = self.request.user.groups.filter(name='common').exists()
        return index

class PostDelete(PermissionRequiredMixin, DeleteView):
    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    permission_required = ('news.delete_post',)
    success_url = '/news/'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='author').exists()
        return context

    def get_index_data(self, **kwargs):
        index = super().get_context_data(**kwargs)
        index['is_not_authorized'] = not self.request.user.groups.filter(name='common').exists()
        return index


class ProtectedView(LoginRequiredMixin, TemplateView):
    template_name = 'news_edit.html'

@login_required
def upgradeMe(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
    return redirect('/')