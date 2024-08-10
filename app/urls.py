from django.urls import path, reverse, reverse_lazy
from django.views.generic import RedirectView

from .views import course_views, graph_visualization_views, teaches_views, topic_views, covers_views, \
    knowledge_area_views, matrix_views

app_name = "app"
urlpatterns = [
    path("", RedirectView.as_view(url=reverse_lazy('app:courses.list')), name="home"),


    path("data-entry/courses/", course_views.courses_list, name="courses.list"),
    path("courses/<str:course_uid>/get-topics/", course_views.get_topics, name="courses.get_topics"),
    path("courses/store/", course_views.store, name="courses.store"),
    path("courses/<str:course_uid>/update/", course_views.update, name="courses.update"),
    path("courses/<str:course_uid>/destroy/", course_views.destroy, name="courses.destroy"),


    path("data-entry/topics/", topic_views.topics_list, name="topics.list"),
    path("topics/<str:topic_uid>/get-courses/", topic_views.get_courses, name="topics.get_courses"),
    path("topics/<str:topic_uid>/get-knowledge-areas/", topic_views.get_knowledge_areas, name="topics.get_knowledge_areas"),
    path("topics/store/", topic_views.store, name="topics.store"),
    path("topics/<str:topic_uid>/update/", topic_views.update, name="topics.update"),
    path("topics/<str:topic_uid>/destroy/", topic_views.destroy, name="topics.destroy"),


    path("data-entry/knowledge-areas/", knowledge_area_views.knowledge_areas_list, name="knowledge_areas.list"),
    path("knowledge-areas/<str:knowledge_area_uid>/get-topics/", knowledge_area_views.get_topics, name="knowledge_areas.get_topics"),
    path("knowledge-areas/store/", knowledge_area_views.store, name="knowledge_areas.store"),
    path("knowledge-areas/<str:knowledge_area_uid>/update/", knowledge_area_views.update, name="knowledge_areas.update"),
    path("knowledge-areas/<str:knowledge_area_uid>/destroy/", knowledge_area_views.destroy, name="knowledge_areas.destroy"),


    path("teaches/store/", teaches_views.store, name="teaches.store"),
    path("teaches/<str:teaches_uid>/update/", teaches_views.update, name="teaches.update"),
    path("teaches/<str:teaches_uid>/destroy/", teaches_views.destroy, name="teaches.destroy"),


    path("covers/store/", covers_views.store, name="covers.store"),
    path("covers/<str:covers_uid>/update/", covers_views.update, name="covers.update"),
    path("covers/<str:covers_uid>/destroy/", covers_views.destroy, name="covers.destroy"),


    path("graph-visualization/", graph_visualization_views.view_graph_visualization, name="graph_visualization"),
    path("matrix/", matrix_views.view_courses_and_topics_matrix, name="matrix.courses_and_topics"),
]