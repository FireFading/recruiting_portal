from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from users.forms import CustomUserCreationForm, MessageForm, ProfileForm, SkillForm

from users.models import Profile, Skill
from users.utils import paginate_profiles, search_profiles


@login_required(login_url="login")
def profiles(request):
    profiles, search_query = search_profiles(request)
    custom_range, profiles = paginate_profiles(request, profiles, 6)
    context = {
        "profiles": profiles,
        "search_query": search_query,
        "custom_range": custom_range,
    }

    return render(request, "users/profiles.html", context)


@login_required(login_url="login")
def user_profile(request, pk):
    profile = Profile.objects.get(pk=pk)
    main_skills = profile.skills.all()[:2]
    extra_skills = profile.skills.all()[2:]
    context = {
        "profile": profile,
        "extra_skills": extra_skills,
        "main_skills": main_skills,
    }

    return render(request, "users/user_profile.html", context)


@login_required(login_url="login")
def profiles_by_skills(request, skill_slag):
    skill = get_object_or_404(Skill.objects.all(), slug=skill_slag)
    profiles = Profile.objects.filter(skills__in=[skill])
    context = {
        "profiles": profiles,
    }
    return render(request, "users/profiles.html", context)


@login_required(login_url="login")
def user_account(request):
    profile = request.user.profile
    skills = profile.skills.all()
    projects = profile.projects.all()

    context = {
        "profile": profile,
        "skills": skills,
        "projects": projects,
    }
    return render(request, "users/user_profile.html", context)


@login_required(login_url="login")
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("account")

    context = {
        "form": form,
    }
    return render(request, "users/profile_form.html", context)


@login_required(login_url="login")
def create_skill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill_slug = request.POST.get("slug")
            skill_description = request.POST.get("description")
            profile.skills.get_or_create(
                name=skill, slug=skill_slug, description=skill_description
            )
            messages.success(request, "Навык добавлен")
            return redirect("account")

    context = {"form": form}
    return render(request, "users/skill_form.html", context)


def register_user(request):
    page = "register"
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            # profile = Profile.objects.create(user=user, name=user.username, email=user.email)
            # profile.save()

            messages.success(request, "Account successfully registered!")
            login(request, user)
            return redirect("edit-account")
        else:
            messages.info(request, "Something wrong, please try again")

    context = {"form": form, "page": page}
    return render(request, "users/login_register.html", context)


@login_required(login_url="login")
def delete_skill(request, skill_slug):
    skill = Skill.objects.get(slug=skill_slug)
    if request.method == "POST":
        skill.delete()
        return redirect("account")

    context = {"object": skill}
    return render(request, "users/delete.html", context)


@login_required(login_url="login")
def update_skill(request, skill_slug):
    skill = Skill.objects.get(slug=skill_slug)
    form = SkillForm(instance=skill)

    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect("account")
    context = {
        "form": form,
    }
    return render(request, "users/skill_form.html", context)


def login_user(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("account")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username)
        except Exception:
            messages.error(request, "User doesn't exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET["next"] if "next" in request.GET else "account")

        else:
            messages.error(request, "Wrong username or password")
    context = {"page": page}
    return render(request, "users/login_register.html", context)


@login_required(login_url="login")
def logout_user(request):
    logout(request)
    messages.info(request, "You successfully logged out")
    return redirect("login")


@login_required(login_url="login")
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {"messageRequests": messageRequests, "unreadCount": unreadCount}
    return render(request, "users/inbox.html", context)


@login_required(login_url="login")
def view_message(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {"message": message}
    return render(request, "users/message.html", context)


def create_message(request, username):
    recipient = Profile.objects.get(name=username)
    form = MessageForm()

    try:
        sender = request.user.profile
    except Exception:
        sender = None

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, "Your message was successfully sent!")
            return redirect("profile", pk=recipient.name)

    context = {"recipient": recipient, "form": form}
    return render(request, "users/message_form.html", context)
