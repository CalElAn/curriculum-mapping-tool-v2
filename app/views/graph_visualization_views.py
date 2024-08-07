from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from inertia import inertia
from django.core.paginator import Paginator
from neomodel import Q
import json
from inertia.utils import InertiaJsonEncoder
from pprint import pprint
from django_rulebase.validator import Validator
from app.cypher_queries import get_nodes_with_relationships
from app.helpers import NeomodelAwareJsonEncoder, validate, redirect_back
from app.models import (
    Topic,
    Course,
    relationship_levels,
    Teaches,
    Covers,
    KnowledgeArea,
    IsPrerequisiteOf,
)


@inertia("GraphVisualization")
@require_GET
def view_graph_visualization(request):
    courses_teaches_topics = get_nodes_with_relationships(Course, Teaches, Topic)

    courses = [i["Course"] for i in courses_teaches_topics]

    topics_covers_knowledge_areas = get_nodes_with_relationships(
        Topic, Covers, KnowledgeArea
    )

    knowledge_areas = [i["KnowledgeArea"] for i in topics_covers_knowledge_areas]

    return {
        "courses": list(
            {getattr(course, "uid"): course for course in courses}.values()
        ),
        "topics": Topic.nodes.all(),
        "coursesWithTopics": courses_teaches_topics,
        "knowledgeAreas": list(
            {
                getattr(knowledge_area, "uid"): knowledge_area
                for knowledge_area in knowledge_areas
            }.values()
        ),
        "knowledgeAreasWithTopics": topics_covers_knowledge_areas,
        "prerequisiteCourses": get_nodes_with_relationships(
            Course, IsPrerequisiteOf, Course
        ),
        "levels": list(relationship_levels.values()),
    }
