from django import forms
from django.forms import ModelForm
from .models import Book, Comment, AdditionalComments



class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = [
            'name',
            'web',
            'price',
            'picture',
        ]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class AdditionalCommentForm(forms.ModelForm):
    class Meta:
        model = AdditionalComments
        fields = ['text']
