from django import forms
from .models import BookReview, Book


class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ["comment", "stars_given"]
        

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'description', 'isbn',]
        