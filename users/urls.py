from django.urls import path

from users import views


urlpatterns = [
    path("", views.profiles, name="profiles"),
    path("profile/<str:pk>", views.user_profile, name="profile"),
    path("skill/<str:skill_slag>", views.profiles_by_skills, name="skill"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register_user, name="register"),
    path("account/", views.user_account, name="account"),
    path("edit-account/", views.edit_account, name="edit-account"),
    path("create-skill/", views.create_skill, name="create-skill"),
    path("update-skill/<slug:skill_slug>/", views.update_skill, name="update-skill"),
    path("delete-skill/<slug:skill_slug>/", views.delete_skill, name="delete-skill"),
    path("inbox/", views.inbox, name="inbox"),
    path("create-message/<str:username>", views.create_message, name="create-message"),
    path("message/<str:pk>", views.view_message, name="message"),
]
