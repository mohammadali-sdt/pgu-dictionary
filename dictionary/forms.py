from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Suggest, Comment


class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggest
        fields = '__all__'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('firstname', 'lastname', 'email', 'text')
        widgets = {
            'firstname': forms.TextInput(
                attrs={'required': 'required', 'placeholder': _('Your firstname'), 'class': "comment-form__input"}),
            'lastname': forms.TextInput(
                attrs={'placeholder': _('Your lastname'), 'class': "comment-form__input"}),
            'email': forms.EmailInput(
                attrs={'placeholder': _('Your email'), 'class': "comment-form__input"}),
            'text': forms.Textarea(
                attrs={'required': 'required', 'cols': '10', 'rows': '5', 'placeholder': _('Your comment'),
                       'class': "comment-form__textarea"}),
        }
