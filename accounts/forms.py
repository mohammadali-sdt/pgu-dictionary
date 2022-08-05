from django import forms
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _

MIN_LENGTH_PASSWORD = 8
MAX_LENGTH_PASSWORD = 32


class UserRegistrationForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(),
                                   required=True,
                                   widget=forms.Select(attrs={'class': "signup-form__select"}),
                                   label=_('group'),
                                   empty_label=_("انتخاب گروه")
                                   )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': _('Password'), 'class': "signup-form__input"}),
        required=True,
        label=_('password'))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': _('Confirm Password'), 'class': "signup-form__input"}), required=True,
        label=_('password confirm'))

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'username', 'email', 'password',
            'password2',
            'group')
        help_texts = {
            'username': '',
        }
        widgets = {
            'first_name': forms.TextInput(
                attrs={'required': 'required', 'placeholder': _('Firstname'), 'class': "signup-form__input"}),
            'last_name': forms.TextInput(
                attrs={'required': 'required', 'placeholder': _('Lastname'), 'class': "signup-form__input"}),
            'email': forms.EmailInput(
                attrs={'required': 'required', 'placeholder': _('Email'), 'class': "signup-form__input"}),
            'username': forms.TextInput(
                attrs={'required': 'required', 'placeholder': _('Username'), 'class': "signup-form__input"}),
        }
        labels = {
            'first_name': _('first_name'),
            'last_name': _('last_name'),
            'username': _('username'),
            'email': _('email'),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        password_length = len(cd.get('password'))
        if cd.get('password') != cd.get('password2'):
            raise forms.ValidationError(_('Password\'s does not match.'))
        if password_length < MIN_LENGTH_PASSWORD or password_length > MAX_LENGTH_PASSWORD:
            raise forms.ValidationError(
                _('Password length must between 8 to 32.'))
        return cd.get('password')

    # def clean_password(self):
    #     cd = self.cleaned_data
    #     password_length = len(cd['password'])
    #     if password_length < 8 or password_length > 32:
    #         raise forms.ValidationError(
    #             'Password length must between 8 to 32.')
    #     return cd['password']

    def clean_email(self):
        cd = self.cleaned_data
        if cd['email'].strip() == '':
            raise forms.ValidationError(_('This field is required.'))
        if User.objects.filter(email=cd['email']).exists():
            raise forms.ValidationError(_('User with that email already exist.'))
        return cd['email']

    def clean_first_name(self):
        cd = self.cleaned_data
        if cd['first_name'].strip() == '':
            raise forms.ValidationError(_('This field is required.'))
        return cd['first_name']

    def clean_last_name(self):
        cd = self.cleaned_data
        if cd['last_name'].strip() == '':
            raise forms.ValidationError(_('This field is required.'))
        return cd['last_name']
