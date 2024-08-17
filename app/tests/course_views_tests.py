import json

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings, Client
from inertia.test import InertiaTestCase
from app.helpers import get_env, items_per_page, NeomodelAwareJsonEncoder
from django.urls import reverse
from neomodel import db, config, clear_neo4j_database, DoesNotExist

from app.models import relationship_levels, Course
from app.tests.helpers import (
    create_and_login_test_user,
    create_courses,
    create_topics,
    client_get,
    create_and_login_test_superuser,
    set_up,
)


class CourseViewsTestCase(InertiaTestCase):
    def setUp(self):
        set_up(InertiaTestCase, self)

    def test_courses_list_has_correct_props(self):
        create_and_login_test_user(self)
        create_courses(5)
        create_topics(3)

        props = client_get(self, reverse("app:courses.list"))

        self.assertComponentUsed("Course/Form")

        self.assertEquals(len(props["initialCourses"]), 5)
        self.assertEquals(len(props["allTopics"]), 3)
        self.assertEquals(props["filter"], "")
        self.assertEquals(props["levels"], list(relationship_levels.values()))
        self.assertTrue(props["pageObj"])

    def test_courses_list_is_ordered_by_number(self):
        create_and_login_test_user(self)

        Course(title="bar", number=456).save()
        Course(title="baz", number=789).save()
        Course(title="foo", number=123).save()

        props = client_get(self, reverse("app:courses.list"))

        self.assertEquals(props["initialCourses"][0]["number"], 123)
        self.assertEquals(props["initialCourses"][1]["number"], 456)
        self.assertEquals(props["initialCourses"][2]["number"], 789)

    def test_courses_list_can_be_filtered(self):
        create_and_login_test_user(self)

        Course(title="foo", number=123).save()
        Course(title="bar", number=456).save()
        Course(title="baz", number=789).save()

        props = client_get(self, reverse("app:courses.list") + "?filter=ar")

        self.assertEquals(len(props["initialCourses"]), 1)
        self.assertEquals(props["initialCourses"][0]["title"], "bar")

        props = client_get(self, reverse("app:courses.list") + "?filter=8")

        self.assertEquals(len(props["initialCourses"]), 1)
        self.assertEquals(props["initialCourses"][0]["number"], 789)

    def test_courses_list_can_be_paginated(self):
        create_and_login_test_user(self)

        create_courses(13)

        props = client_get(self, reverse("app:courses.list") + "?page=2")

        self.assertEquals(len(props["initialCourses"]), 13 - items_per_page)
        self.assertTrue(props["pageObj"])

        # TODO: separate tests for test_helpers where I test pagination
        # page_obj = props["pageObj"]
        #
        # self.assertEquals(page_obj.hasPrevious, True)
        # self.assertEquals(page_obj.previousPageNumber, 2)

    def test_get_courses(self):
        courses = create_courses(2)

        course = courses[0]

        topics = create_topics(3)

        for topic in topics:
            course.teaches.connect(topic, {"level": relationship_levels["beginner"]})

        create_and_login_test_user(self)

        json_response = self.client.get(
            reverse("app:courses.get_topics", args=[course.uid])
        ).json()

        self.assertEquals(len(json_response), 3)

        json_response = self.client.get(
            reverse("app:courses.get_topics", args=[courses[1].uid])
        ).json()

        self.assertEquals(len(json_response), 0)

    def test_only_superusers_can_create_update_and_delete_courses(self):
        create_and_login_test_user(self)

        response_json = self.client.post(
            reverse("app:courses.store"),
            content_type="application/json",
        ).json()

        self.assertEquals(
            response_json, {"message": "This action can only be performed by an admin"}
        )

        for route in ("update", "destroy"):
            response_json = self.client.post(
                reverse(f"app:courses.{route}", args=["foo"]),
                content_type="application/json",
            ).json()

            self.assertEquals(
                response_json,
                {"message": "This action can only be performed by an admin"},
            )

    def test_create_course_validation(self):
        create_and_login_test_superuser(self, client="inertia")

        response = self.inertia.post(
            reverse("app:courses.store"),
            json.dumps({"number": "456", "title": "foo"}),
            content_type="application/json",
        )

        self.assertEquals(
            response.client.session["errors"],
            {"number": [" validation error for number because of integer "]},
        )

        response = self.inertia.post(
            reverse("app:courses.store"),
            # passing an empty string should fail validation, but it doesn't.
            # Have submitted an issue to the library's GitHub https://github.com/mojtabaasadi/django-rulebase/issues/5#issue-2471629120
            json.dumps({"number": None, "title": None}),
            content_type="application/json",
        )
        self.assertEquals(
            response.client.session["errors"],
            {"number": ["is required"], "title": ["is required"]},
        )

    def test_create_course(self):
        create_and_login_test_superuser(self, client="inertia")

        self.inertia.post(
            reverse("app:courses.store"),
            json.dumps({"number": 456, "title": "foo"}),
            content_type="application/json",
        )

        courses = Course.nodes.all()

        self.assertEquals(len(courses), 1)
        self.assertEquals(courses[0].title, "foo")
        self.assertEquals(courses[0].number, 456)

    def test_update_course(self):
        create_and_login_test_superuser(self, client="inertia")

        course = create_courses(3)[0]

        self.inertia.post(
            reverse("app:courses.update", args=[course.uid]),
            json.dumps({"number": 456, "title": "foo"}),
            content_type="application/json",
        )

        course = Course.nodes.get(uid=course.uid)

        self.assertEquals(course.title, "foo")
        self.assertEquals(course.number, 456)

    def test_delete_course(self):
        create_and_login_test_superuser(self, client="inertia")

        course = create_courses(3)[0]

        self.inertia.post(
            reverse("app:courses.destroy", args=[course.uid]),
            content_type="application/json",
        )

        with self.assertRaises(DoesNotExist):
            Course.nodes.get(uid=course.uid)

        self.assertEquals(len(Course.nodes.all()), 2)
