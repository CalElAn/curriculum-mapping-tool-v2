from django.urls import path, reverse, reverse_lazy
from django.views.generic import RedirectView

from .views import course_views, graph_visualization_views, teaches_views

app_name = "app"
urlpatterns = [
    path("", RedirectView.as_view(url=reverse_lazy('app:courses.list')), name="home"),

    path("data-entry/courses/", course_views.courses_list, name="courses.list"),
    path("courses/<str:course_uid>/get-topics/", course_views.get_topics, name="courses.get_topics"),
    path("courses/store/", course_views.store, name="courses.store"),
    path("courses/<str:course_uid>/update/", course_views.update, name="courses.update"),
    path("courses/<str:course_uid>/destroy/", course_views.destroy, name="courses.destroy"),

    path("teaches/store/", teaches_views.store, name="teaches.store"),
    path("teaches/<str:teaches_uid>/update/", teaches_views.update, name="teaches.update"),
    path("teaches/<str:teaches_uid>/destroy/", teaches_views.destroy, name="teaches.destroy"),

    path("graph-visualization/", graph_visualization_views.view_graph_visualization, name="graph_visualization"),
]