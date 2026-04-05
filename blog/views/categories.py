from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from blog.forms import CategoryForm
from blog.mixins import CategoryOwnerAdminMixin
from blog.models import Category


class CategoryListView(ListView):
    model = Category
    template_name = 'blog/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.select_related('created_by').annotate(article_count=Count('articles'))


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'blog/category_form.html'
    success_url = reverse_lazy('category_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class CategoryUpdateView(CategoryOwnerAdminMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'blog/category_form.html'
    success_url = reverse_lazy('category_list')


class CategoryDeleteView(CategoryOwnerAdminMixin, DeleteView):
    model = Category
    template_name = 'blog/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')
