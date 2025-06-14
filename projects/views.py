from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Project, Tag
from .forms import ProjectForm

# Create your views here.



def projects(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    tags = Tag.objects.filter(name__icontains=search_query)

    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(owner__name__icontains=search_query) |
        Q(tags__in=tags)
    )

    context = {
        'projects': projects,
        'search_query' : search_query
    }
    return render(request , 'projects/projects.html' , context)

from django.shortcuts import get_object_or_404

def project(request, pk):
    projObject = get_object_or_404(Project, pk=pk)
    return render(request, 'projects/single-projects.html', {'project': projObject})

@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST , request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')

    context = {'form' : form}
    return render(request , 'projects/project-form.html' ,context)


@login_required(login_url="login")
def updateProject(request , pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST , request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form' : form}
    return render(request , 'projects/project-form.html' ,context)


@login_required(login_url="login")
def deleteProject(request , pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context = {'object' : project}
    return render(request , 'delete-template.html' , context)