from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, SkillForm, ProfileForm

# Create your views here.


def profiles(requests):
    profiles = Profile.objects.all()
    context = {"profiles": profiles}

    return render(requests, "users/profiles.html", context)


def userProfile(requests, pk):
    profileObj = Profile.objects.get(id=pk)
    context = {
        "profile": profileObj,
    }

    return render(requests, "users/user-profile.html", context)


def loginUser(requests):
    page = "login"

    if requests.user.is_authenticated:
        return redirect("profiles")

    if requests.method == "POST":
        username = requests.POST["username"]
        password = requests.POST["password"]

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(requests, "Username does not exist")

        user = authenticate(requests, username=username, password=password)

        if user is not None:
            # <-- login function creates a session on the database for the user
            login(requests, user)
            return redirect("profiles")
        else:
            messages.error(requests, "Username or Password was incorrect.")

    context = {
        "page": page,
    }
    return render(requests, "users/login_register.html", context)


def logoutUser(requests):
    logout(requests)
    messages.success(requests, "User was succesfully logged out")
    return redirect("login")


def registerUser(requests):
    page = "register"
    form = CustomUserCreationForm()

    if requests.method == "POST":
        form = CustomUserCreationForm(requests.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()  # <-- this removes the
            # event where upper and lower case versions of a username exist in the same database
            user.save()

            messages.success(requests, "user account was created")
            login(requests, user)
            return redirect("profiles")
        else:
            messages.error(requests, "An error has occurred.")

    context = {
        "page": page,
        "form": form,
    }
    return render(requests, "users/login_register.html", context)


@login_required(login_url="login")
def userAccount(requests):
    profile = requests.user.profile
    context = {
        "profile": profile,
    }

    return render(requests, "users/account.html", context)


@login_required(login_url="login")
def createSkill(requests):
    form = SkillForm()

    context = {"form": form}
    return render(requests, "users/create_update.html", context)


@login_required(login_url="login")
def updateSkill(requests):

    context = {}
    return render(requests, "users/create_update.html", context)


@login_required(login_url="login")
def deleteSkill(requests):

    context = {}
    return render(requests, "users/delete_skill.html", context)


@login_required(login_url="login")
def editAccount(requests):
    form = ProfileForm()
    profile = requests.user.profile

    if requests.method == "POST":
        form = ProfileForm(requests.POST, requests.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect("userAccount")

    context = {"form": form}
    return render(requests, "users/profile_form.html", context)
