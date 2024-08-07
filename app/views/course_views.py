import json
from datetime import datetime

from django.shortcuts import render, redirect
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
from app.helpers import (
    NeomodelAwareJsonEncoder,
    validate,
    redirect_back,
    paginate,
    get_page_obj_props,
    validate_unique_node_attribute,
)
from app.models import Topic, Course, relationship_levels, Teaches


@inertia("Course/Form")
@require_GET
def courses_list(request):
    request_filter = request.GET.get("filter", "")

    courses = Course.nodes.order_by("number").all()

    filtered_courses = []
    for course in courses:
        if (request_filter.lower() in course.title.lower()) or str(
            request_filter
        ) in str(course.number):
            filtered_courses.append(course)

    paginator, page_obj = paginate(filtered_courses, request.GET.get("page", 1))

    return {
        "initialCourses": page_obj.object_list,
        "pageObj": get_page_obj_props(page_obj, paginator),
        "allTopics": Topic.nodes.order_by("name").all(),
        "levels": list(relationship_levels.values()),
        "filter": request_filter,
    }


@require_GET
def get_topics(request, course_uid):
    return JsonResponse(
        get_nodes_with_relationships(
            Course, Teaches, Topic, Course, course_uid, "name", Topic
        ),
        safe=False,
        encoder=NeomodelAwareJsonEncoder,
    )


@require_POST
def store(request):
    validation_results = validate(
        request,
        {
            "number": "required|integer",
            "title": "required",
        },
    )

    validate_unique_node_attribute(Course, "number", request.body_json["number"])

    course = Course(
        **{key: request.body_json[key] for key in validation_results}
    ).save()

    request.session["data"] = {"uid": course.uid}

    return redirect_back(request)


@require_POST
def update(request, course_uid):
    validation_results = validate(
        request,
        {
            "number": "required|integer",
            "title": "required",
        },
    )

    course = Course.nodes.get(uid=course_uid)

    validate_unique_node_attribute(
        Course, "number", request.body_json["number"], course
    )

    for key in validation_results:
        setattr(course, key, request.body_json[key])

    course.save()

    return redirect_back(request)


@require_POST
def destroy(request, course_uid):
    Course.nodes.get(uid=course_uid).delete()

    return redirect_back(request)
