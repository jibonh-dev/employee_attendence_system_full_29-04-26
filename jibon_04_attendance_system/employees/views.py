from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date

from .forms import RegisterForm, LoginForm, ProfileForm, CustomPasswordChangeForm,AttendanceForm
from .models import ProfileModel,AttendanceModel

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            ProfileModel.objects.create(user=user)

            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'myapp/Auth/register.html', {'form': form})


def login_view(request):
    form = LoginForm(request, data=request.POST or None)
    if form.is_valid():
        login(request, form.get_user())
        return redirect('profile')
    return render(request, 'myapp/Auth/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request):
    profile, created = ProfileModel.objects.get_or_create(user=request.user)
    return render(request, 'myapp/Auth/profile.html', {'profile': profile})


@login_required
def edit_profile(request):
    profile, created = ProfileModel.objects.get_or_create(user=request.user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)

    if form.is_valid():
        form.save()
        return redirect('profile')

    return render(request, 'myapp/master/master_form.html', {
        'form': form,
        'Title': 'Edit Profile',
        'submit_btn': 'Update'
    })


@login_required
def change_password_view(request):
    form = CustomPasswordChangeForm(user=request.user, data=request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('login')

    return render(request, 'myapp/master/master_form.html', {
        'form': form,
        'Title': 'Change Password',
        'submit_btn': 'Update Password'
    })


@login_required
def add_attendance(request):
    if not request.user.is_superuser:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = AttendanceForm()

    return render(request, 'myapp/master/master_form.html', {'form': form})


# -------------------------
# UPDATE ATTENDANCE
# -------------------------
@login_required
def update_attendance(request, pk):
    if not request.user.is_superuser:
        return redirect('dashboard')

    attendance = get_object_or_404(AttendanceModel, id=pk)

    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = AttendanceForm(instance=attendance)

    return render(request, 'myapp/master/master_form.html', {'form': form})


# -------------------------
# DELETE ATTENDANCE
# -------------------------
@login_required
def delete_attendance(request, pk):
    if request.user.is_superuser:
        attendance = get_object_or_404(AttendanceModel, id=pk)
        attendance.delete()

    return redirect('dashboard')




@login_required
def dashboard(request):

    if request.user.is_superuser:
        # Superuser sees ALL records
        records = AttendanceModel.objects.all()
        present = AttendanceModel.objects.filter(status='Present').count()
        absent = AttendanceModel.objects.filter(status='Absent').count()

    else:
        # Normal user sees only their records
        profile = request.user.profile
        records = profile.attendances.all()
        present = profile.attendances.filter(status='Present').count()
        absent = profile.attendances.filter(status='Absent').count()

    return render(request, 'crud/dashboard.html', {
        'records': records,
        'present': present,
        'absent': absent
    })