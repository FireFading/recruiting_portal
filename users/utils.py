from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q

from users.models import Profile, Skill


def paginate_profiles(request, profiles, results):
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

    left_index = int(page) - 4

    left_index = max(left_index, 1)
    right_index = int(page) + 5

    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    custom_range = range(left_index, right_index)

    return custom_range, profiles


def search_profiles(request):
    search_query = request.GET.get("search_query") or ""
    skills = Skill.objects.filter(name__icontains=search_query)
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query)
        | Q(intro__icontains=search_query)
        | Q(skills__in=skills)
    )
    return profiles, search_query
