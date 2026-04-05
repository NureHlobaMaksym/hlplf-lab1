from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from accounts.models import User


class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField(label='Електронна пошта')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': 'Невірний email або пароль.',
        'inactive': 'Акаунт не активний.',
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
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
        if 'display_name' in self.fields:
            self.fields['display_name'].widget.attrs.update({'maxlength': '80'})

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        if email and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise ValidationError(self.error_messages['invalid_login'], code='invalid_login')
            if not self.user_cache.is_active:
                raise ValidationError(self.error_messages['inactive'], code='inactive')
        return cleaned_data

    def get_user(self):
        return getattr(self, 'user_cache', None)


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторіть пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['display_name', 'email']
        labels = {
            'display_name': "Ім'я",
            'email': 'Електронна пошта',
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
        self.fields['password1'].widget.attrs.update(
            {
                'class': 'w-full rounded border px-3 py-2 focus:outline-none',
                'style': 'border-color: var(--border); background: var(--surface-strong); color: var(--text);',
            }
        )
        self.fields['password2'].widget.attrs.update(
            {
                'class': 'w-full rounded border px-3 py-2 focus:outline-none',
                'style': 'border-color: var(--border); background: var(--surface-strong); color: var(--text);',
            }
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Паролі не збігаються.')
        if password2 and len(password2) < 6:
            raise ValidationError('Пароль має бути мінімум 6 символів.')
        return password2

    def clean_display_name(self):
        display_name = self.cleaned_data.get('display_name', '').strip()
        if not display_name:
            raise ValidationError("Ім'я є обов'язковим.")
        return display_name

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label='Пароль')

    class Meta:
        model = User
        fields = ['email', 'display_name', 'password', 'is_active', 'is_staff']
