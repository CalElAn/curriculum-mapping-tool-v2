import json

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from inertia.test import InertiaTestCase
from neomodel import DoesNotExist, clear_neo4j_database, config, db

from app.cypher_queries import get_nodes_with_relationships
from app.helpers import NeomodelAwareJsonEncoder, get_env, items_per_page
from app.models import (Course, Covers, KnowledgeArea, Teaches, Topic,
                        relationship_levels)
from app.tests.helpers import (client_get, create_and_login_test_superuser,
                               create_and_login_test_user, create_courses,
                               create_knowledge_areas, create_topics, set_up)


class TeachesViewsTestCase(InertiaTestCase):
    def setUp(self):
        set_up(InertiaTestCase, self)

    def test_create_teaches_validation(self):
        create_and_login_test_user(self, client="inertia")

        response = self.inertia.post(
            reverse("app:teaches.store"),
            json.dumps({"level": None, "tools": None, "comments": None}),
            content_type="application/json",
        )
        self.assertEquals(
            response.client.session["errors"],
            {
                "level": ["is required"],
                "tools": ["is required"],
                "comments": ["is required"],
            },
        )

        course = Course(number=123, title="foo").save()
        topic = Topic(title="bar").save()
        course.teaches.connect(topic, {"level": relationship_levels["beginner"]})

        response = self.inertia.post(
            reverse("app:teaches.store"),
            json.dumps(
                {
                    "course_uid": course.uid,
                    "topic_uid": topic.uid,
                    "level": relationship_levels["beginner"],
                    "tools": "foo",
                    "comments": "bar",
                }
            ),
            content_type="application/json",
        )
        self.assertEquals(
            response.client.session["errors"],
            {"relationship": ["must be unique"]},
        )

    def test_create_teaches(self):
        create_and_login_test_user(self, client="inertia")

        course = Course(number=123, title="foo").save()
        topic = Topic(title="bar").save()

        self.inertia.post(
            reverse("app:teaches.store"),
            json.dumps(
                {
                    "course_uid": course.uid,
                    "topic_uid": topic.uid,
                    "level": relationship_levels["beginner"],
                    "tools": "foo",
                    "comments": "bar",
                }
            ),
            content_type="application/json",
        )

        course_teaches_topic = get_nodes_with_relationships(
            Course, Teaches, Topic, Course, course.uid
        )

        teaches = course_teaches_topic[0]["TEACHES"]

        self.assertEquals(len(course_teaches_topic), 1)
        self.assertEquals(teaches.level, relationship_levels["beginner"])
        self.assertEquals(teaches.tools, "foo")
        self.assertEquals(teaches.comments, "bar")

    def test_update_teaches_validation(self):
        create_and_login_test_user(self, client="inertia")

        course = Course(number=123, title="foo").save()
        topic = Topic(title="bar").save()
        course.teaches.connect(topic, {"level": relationship_levels["beginner"]})

        teaches = get_nodes_with_relationships(
            Course, Teaches, Topic, Course, course.uid
        )[0]["TEACHES"]

        response = self.inertia.post(
            reverse("app:teaches.update", args=[teaches.uid]),
            json.dumps({"level": None, "tools": None, "comments": None}),
            content_type="application/json",
        )
        self.assertEquals(
            response.client.session["errors"],
            {
                "level": ["is required"],
                "tools": ["is required"],
                "comments": ["is required"],
            },
        )

    def test_update_teaches(self):
        create_and_login_test_user(self, client="inertia")

        course = Course(number=123, title="foo").save()
        topic = Topic(title="bar").save()
        course.teaches.connect(
            topic,
            {
                "level": relationship_levels["beginner"],
                "tools": "tool 1",
                "comments": "comment 1",
            },
        )

        teaches = get_nodes_with_relationships(
            Course, Teaches, Topic, Course, course.uid
        )[0]["TEACHES"]

        self.inertia.post(
            reverse("app:teaches.update", args=[teaches.uid]),
            json.dumps(
                {
                    "level": relationship_levels["intermediate"],
                    "tools": "tool 22",
                    "comments": "comment 22",
                }
            ),
            content_type="application/json",
        )

        teaches = get_nodes_with_relationships(
            Course, Teaches, Topic, Course, course.uid
        )[0]["TEACHES"]

        self.assertEquals(teaches.level, relationship_levels["intermediate"])
        self.assertEquals(teaches.tools, "tool 22")
        self.assertEquals(teaches.comments, "comment 22")

    def test_delete_teaches(self):
        create_and_login_test_user(self, client="inertia")

        course = Course(number=123, title="foo").save()
        topic = Topic(title="bar").save()
        course.teaches.connect(
            topic,
            {
                "level": relationship_levels["beginner"],
            },
        )

        teaches = get_nodes_with_relationships(
            Course, Teaches, Topic, Course, course.uid
        )[0]["TEACHES"]

        self.inertia.post(
            reverse("app:teaches.destroy", args=[teaches.uid]),
            content_type="application/json",
        )

        course_teaches_topic = get_nodes_with_relationships(
            Course, Teaches, Topic, Course, course.uid
        )

        self.assertEquals(len(course_teaches_topic), 0)
