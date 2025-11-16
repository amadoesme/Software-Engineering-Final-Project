from django import forms
from django.forms import ModelForm
from .models import Book, Rating


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = [
            'name',
            'web',
            'price',
            'picture',
        ]
class RatingForm(ModelForm):
    value = forms.IntegerField(
        label = 'Your Rating (1-5)',
        min_value = 1,
        max_value = 5,
        widget = forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Enter a number between 1 and 5' })
    )
    #model = Book
    #fields = [
    #    label = 'Your Rating (1-5)',
    #min_value = 1,
    #max_value = 5
    #widget = forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter a number between 1 and 5'})
    #]

    class Meta:
        model = Rating
        fields = ['value']