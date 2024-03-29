from django.urls import path

from projects import views


urlpatterns = [
    path("", views.all_projects, name="projects"),
    path("project/<str:pk>/", views.project, name="project"),
    path("create-project/", views.create_project, name="create-project"),
    path("update-project/<str:pk>/", views.update_project, name="update-project"),
    path("delete-project/<str:pk>/", views.delete_project, name="delete-project"),
    path("tag/<slug:tag_slug>", views.projects_by_tag, name="tag"),
]
