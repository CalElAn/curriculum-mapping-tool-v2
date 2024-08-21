from django.views.decorators.http import (require_GET)
from inertia import inertia

from app.cypher_queries import get_nodes_with_relationships
from app.models import (Course, Covers, KnowledgeArea,
                        Teaches, Topic)


@inertia("Matrix/CoursesAndTopics")
@require_GET
def view_courses_and_topics_matrix(request):
    return {
        "courses": Course.nodes.order_by("number").all(),
        "topics": Topic.nodes.order_by("title").all(),
        "coursesTeachesTopics": get_nodes_with_relationships(Course, Teaches, Topic),
    }


@inertia("Matrix/TopicsAndKnowledgeAreas")
@require_GET
def view_topics_and_knowledge_areas_matrix(request):
    return {
        "topics": Topic.nodes.order_by("title").all(),
        "knowledgeAreas": KnowledgeArea.nodes.order_by("title").all(),
        "topicsCoversKnowledgeAreas": get_nodes_with_relationships(
            Topic, Covers, KnowledgeArea
        ),
    }
