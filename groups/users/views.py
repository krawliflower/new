from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You are now able to log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


from django.contrib.auth.models import Group

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)

        if form.is_valid():
            user = form.save()

            # Update user groups based on subjects and role
            selected_subjects = form.cleaned_data.get('subjects')
            role_group = form.cleaned_data.get('role')
            
            # Clear existing groups and add new ones
            user.groups.clear()
            
            # Add role group if it is selected
            if role_group:
                role_group_obj, created = Group.objects.get_or_create(name=role_group)
                user.groups.add(role_group_obj)
            
            # Add subject groups
            for subject in selected_subjects:
                subject_group, created = Group.objects.get_or_create(name=subject)
                user.groups.add(subject_group)

            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)

    # Retrieve the role group
    role_group = request.user.groups.filter(name__in=['tutor', 'tutee']).first()

    context = {
        'form': form,
        'role_group': role_group,
    }

    return render(request, 'users/profile.html', context)
