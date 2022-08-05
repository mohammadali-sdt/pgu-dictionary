from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test, permission_required
from .forms import UserRegistrationForm


# Create your views here.
# @user_passes_test(lambda user: user.is_active and user.is_superuser, login_url='accounts:login')
@permission_required('auth.can_add_user', raise_exception=True)
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            group = cd['group']
            new_user = form.save(commit=False)
            new_user.set_password(cd['password'])
            new_user.is_staff = True
            new_user.save()
            group.user_set.add(new_user)
            return render(request, 'registration/register_user_success.html')

    else:
        form = UserRegistrationForm()
    return render(request, 'registration/signup.html', {'form': form})
