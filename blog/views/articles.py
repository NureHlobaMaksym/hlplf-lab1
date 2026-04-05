from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from blog.forms import ArticleForm, CommentForm
from blog.mixins import ArticleAuthorOrAdminMixin
from blog.models import Article, Category


class ArticleListView(ListView):
    model = Article
    template_name = 'blog/article_list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        queryset = (
            Article.objects.select_related('category', 'author')
            .annotate(comment_count=Count('comments'))
        )
        category_id = self.kwargs.get('pk')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        sort = self.request.GET.get('sort', 'date')
        if sort not in {'date', 'comments'}:
            sort = 'date'
        direction = self.request.GET.get('dir', 'desc')
        if direction not in {'asc', 'desc'}:
            direction = 'desc'
        order_prefix = '' if direction == 'asc' else '-'

        if sort == 'comments':
            return queryset.order_by(f'{order_prefix}comment_count', f'{order_prefix}published_at')
        return queryset.order_by(f'{order_prefix}published_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.annotate(article_count=Count('articles'))
        context['active_sort'] = self.request.GET.get('sort', 'date')
        context['active_dir'] = self.request.GET.get('dir', 'desc')
        context['active_category'] = self.kwargs.get('pk')
        return context


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/article_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'pk': self.object.pk})


class ArticleUpdateView(LoginRequiredMixin, ArticleAuthorOrAdminMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/article_form.html'

    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'pk': self.object.pk})


class ArticleDeleteView(LoginRequiredMixin, ArticleAuthorOrAdminMixin, DeleteView):
    model = Article
    template_name = 'blog/article_confirm_delete.html'
    success_url = reverse_lazy('article_list')


def article_detail(request: HttpRequest, pk: int) -> HttpResponse:
    article = get_object_or_404(
        Article.objects.select_related('category', 'author').annotate(
            comment_count=Count('comments')
        ),
        pk=pk,
    )
    comments = article.comments.select_related('author')
    user = request.user
    can_manage = user.is_authenticated and (
        (user.is_staff and not (article.author.is_staff and article.author != user))
        or user == article.author
    )

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.article = article
            new_comment.author = request.user
            new_comment.save()
            return redirect('article_detail', pk=article.pk)
    else:
        form = CommentForm()

    return render(
        request,
        'blog/article_detail.html',
        {
            'article': article,
            'comments': comments,
            'comment_form': form,
            'can_manage': can_manage,
        },
    )
