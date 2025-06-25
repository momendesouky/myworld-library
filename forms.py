from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Book, User
from django.core.exceptions import ValidationError
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'category', 'description', 'status', 'photo']

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    is_admin = forms.BooleanField(
        required=False,
        label='Register as Admin'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'is_admin')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if self.cleaned_data['is_admin']:
            user.is_staff = True
            user.is_superuser = True  # Add this for full admin privileges
        if commit:
            user.save()
        return user
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username