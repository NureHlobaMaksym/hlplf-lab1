from django.contrib.auth.mixins import UserPassesTestMixin

from blog.models import Article


class ArticleAuthorOrAdminMixin(UserPassesTestMixin):
    def test_func(self):
        article: Article = self.get_object()
        user = self.request.user
        if not user.is_authenticated:
            return False
        if user.is_staff and article.author.is_staff and article.author != user:
            return False
        return user.is_staff or article.author == user


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff


class CategoryOwnerAdminMixin(UserPassesTestMixin):
    def test_func(self):
        category = self.get_object()
        user = self.request.user
        if not user.is_authenticated:
            return False
        return category.created_by == user
