from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import paginator

from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from .utils import paginateProjects, searchProjects


@login_required(login_url='login')
def all_projects(request):
    projects, search_query = searchProjects(request)
    custom_range, projects = paginateProjects(request, projects, 6)
    context = {
        "projects": projects,
        "search_query": search_query,
        'custom_range': custom_range,
    }
    
    return render(request, 'projects.html', context)


@login_required(login_url='login')
def project(request, pk):
    project = Project.objects.get(pk=pk)
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = project
        review.owner = request.user.profile
        review.save()
        project.getVoteCount
        messages.success(request, 'Your review was successfully saved!')
        
    context = {"project": project}
    return render(request, 'single-project.html', context)


@login_required(login_url='login')
def create_project(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('projects')
    context = {
        'form': form,
    }
    return render(request, 'project_form.html', context)


@login_required(login_url='login')
def update_project(request, pk):
    project = Project.objects.get(pk=pk)
    form = ProjectForm(instance=project)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')
    context = {
        'form': form,
    }
    return render(request, 'project_form.html', context)


@login_required(login_url='login')
def delete_project(request, pk):
    project = Project.objects.get(pk=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    
    context = {
        'object': project
    }
    return render(request, 'delete.html', context)


@login_required(login_url='login')
def projects_by_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    projects = Project.objects.filter(tags__in=[tag])
    
    context = {
        'projects': projects
    }
    return render(request, 'projects.html', context)