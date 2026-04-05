from django import forms
from blog.models import Article, Category, Comment


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['category', 'title', 'body']
        labels = {
            'category': 'Категорія',
            'title': 'Заголовок',
            'body': 'Текст',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update(
                {
                    'class': (
                        'w-full rounded border px-3 py-2 focus:outline-none'
                    )
                }
            )
        for field in self.fields.values():
            field.widget.attrs.update(
                {
                    'style': 'border-color: var(--border); background: var(--surface-strong); color: var(--text);'
                }
            )
        self.fields['title'].widget.attrs.update({'maxlength': '150'})
        self.fields['body'].widget.attrs.update({'maxlength': '6000'})


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {'body': 'Коментар'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update(
                {
                    'class': (
                        'w-full rounded border px-3 py-2 focus:outline-none'
                    )
                }
            )
        for field in self.fields.values():
            field.widget.attrs.update(
                {
                    'style': 'border-color: var(--border); background: var(--surface-strong); color: var(--text);'
                }
            )
        self.fields['body'].widget.attrs.update({'maxlength': '600'})


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        labels = {'name': 'Назва'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update(
                {
                    'class': (
                        'w-full rounded border px-3 py-2 focus:outline-none'
                    )
                }
            )
        for field in self.fields.values():
            field.widget.attrs.update(
                {
                    'style': 'border-color: var(--border); background: var(--surface-strong); color: var(--text);'
                }
            )
        self.fields['name'].widget.attrs.update({'maxlength': '80'})
