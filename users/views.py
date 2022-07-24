from django.shortcuts import render, get_object_or_404

from .models import Profile, Skill

def profiles(request):
    profiles = Profile.objects.all()
    context = {
        'profiles': profiles
    }
    
    return render(request, 'profiles.html', context)


def user_profile(request, pk):
    profile = Profile.objects.get(pk=pk)
    main_skills = profile.skills.all()[:2]
    extra_skills = profile.skills.all()[2:]
    context = {
        'profile': profile,
        'extra_skills': extra_skills,
        'main_skills': main_skills,
    }
    
    return render(request, 'user_profile.html', context)


def profiles_by_skills(request, skill_slag):
    skill = get_object_or_404(Skill.objects.all(), slug=skill_slag)
    profiles = Profile.objects.filter(skills__in=[skill])
    context = {
        'profiles': profiles,
    }
    return render(request, 'profiles.html', context)