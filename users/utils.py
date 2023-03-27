from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q

from .models import Profile, Skill


def paginateProfiles(request, profiles, results):
    page = request.GET.get("page")
    paginator = Paginator(profiles, results)

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    leftIndex = int(page) - 4

    leftIndex = max(leftIndex, 1)
    rightIndex = int(page) + 5

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, profiles


def searchProfiles(request):
    search_query = request.GET.get("search_query") or ""
    skills = Skill.objects.filter(name__icontains=search_query)
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query)
        | Q(intro__icontains=search_query)
        | Q(skills__in=skills)
    )
    return profiles, search_query
