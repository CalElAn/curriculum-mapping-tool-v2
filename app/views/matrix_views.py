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


@inertia("Matrix/CoursesAndTopics")
@require_GET
def view_courses_and_topics_matrix(request):
    return {
        "courses": Course.nodes.order_by("number").all(),
        "topics": Topic.nodes.order_by("name").all(),
        "coursesTeachesTopics": get_nodes_with_relationships(Course, Teaches, Topic),
        "levels": list(relationship_levels.values()),
    }
