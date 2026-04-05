from blog.views.articles import (
    ArticleCreateView,
    ArticleDeleteView,
    ArticleListView,
    ArticleUpdateView,
    article_detail,
)
from blog.views.categories import (
    CategoryCreateView,
    CategoryDeleteView,
    CategoryListView,
    CategoryUpdateView,
)
from blog.views.comments import CommentDeleteView
from blog.views.comments import CommentUpdateView

__all__ = [
    'ArticleCreateView',
    'ArticleDeleteView',
    'ArticleListView',
    'ArticleUpdateView',
    'CategoryCreateView',
    'CategoryDeleteView',
    'CategoryListView',
    'CategoryUpdateView',
    'CommentDeleteView',
    'CommentUpdateView',
    'article_detail',
]
