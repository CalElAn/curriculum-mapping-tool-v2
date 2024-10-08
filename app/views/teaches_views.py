from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST

from app.cypher_queries import (delete_relationship,
                                get_nodes_with_relationships, get_relationship)
from app.helpers import redirect_back, validate
from app.models import Course, Teaches, Topic


@require_POST
def store(request):
    validate(
        request,
        {
            "level": "required",
            "tools": "required",
            "comments": "required",
        },
    )

    courses_teaches_topics = get_nodes_with_relationships(Course, Teaches, Topic)

    request_course_uid = request.body_json["course_uid"]
    request_topic_uid = request.body_json["topic_uid"]

    if list(
        filter(
            lambda item: getattr(item["Course"], "uid") == request_course_uid
            and getattr(item["Topic"], "uid") == request_topic_uid,
            courses_teaches_topics,
        )
    ):
        raise ValidationError({"relationship": "must be unique"})

    teaches = Course.nodes.get(uid=request_course_uid).teaches.connect(
        Topic.nodes.get(uid=request_topic_uid),
        {
            "level": request.body_json["level"],
            "tools": request.body_json["tools"],
            "comments": request.body_json["comments"],
        },
    )

    teaches.save()

    request.session["data"] = {"uid": teaches.uid}

    return redirect_back(request)


@require_POST
def update(request, teaches_uid):
    validate(
        request,
        {
            "level": "required",
            "tools": "required",
            "comments": "required",
        },
    )

    teaches = get_relationship(Teaches, teaches_uid)

    teaches.level = request.body_json["level"]
    teaches.tools = request.body_json["tools"]
    teaches.comments = request.body_json["comments"]

    teaches.save()

    return redirect_back(request)


@require_POST
def destroy(request, teaches_uid):
    delete_relationship(Teaches, teaches_uid)

    return redirect_back(request)
