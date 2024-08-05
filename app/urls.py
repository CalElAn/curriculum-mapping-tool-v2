from django.urls import path
from .views import course_views

app_name = "app"
urlpatterns = [
    path("", course_views.courses_list, name="courses.list"),
    path("data-entry/courses/", course_views.courses_list, name="courses.list"),
    path("courses/<str:course_uid>/get-topics/", course_views.get_topics, name="courses.get_topics"),
    path("courses/store/", course_views.store, name="courses.store"),
    path("courses/<str:course_uid>/update/", course_views.update, name="courses.update"),
    path("courses/<str:course_uid>/destroy/", course_views.destroy, name="courses.destroy"),
]