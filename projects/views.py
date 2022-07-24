from django.shortcuts import render, redirect, get_object_or_404

from .models import Project, Tag
from .forms import ProjectForm


def projects(request):
    projects = Project.objects.all()
    context = {
        "projects": projects,
    }
    
    return render(request, 'projects.html', context)


def project(request, pk):
    project = Project.objects.get(pk=pk)
    context = {"project": project}
    return render(request, 'single-project.html', context)


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


def delete_project(request, pk):
    project = Project.objects.get(pk=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    
    context = {
        'object': project
    }
    return render(request, 'delete.html', context)


def projects_by_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    projects = Project.objects.filter(tags__in=[tag])
    
    context = {
        'projects': projects
    }
    return render(request, 'projects.html', context)