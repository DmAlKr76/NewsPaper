from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.core.paginator import Paginator

class PostsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-id')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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


class PostDetail(DetailView):
    model = Post
    template_name = 'news_.html'
    context_object_name = 'news_'

class PostAdd(CreateView):
    model = Post
    template_name = 'news_add.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)


class PostEdit(UpdateView):
    template_name = 'news_edit.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class PostDelete(DeleteView):
    template_name = 'news_delete.html'
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context