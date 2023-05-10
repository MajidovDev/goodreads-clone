from django import forms
from django.db import models
from books.models import BookReview


class BookReviewForm(forms.ModelForm):
    starts_given = forms.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = BookReview
        fields = ('comment', 'starts_given',)


