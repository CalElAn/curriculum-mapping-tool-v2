import json

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from inertia.test import InertiaTestCase
from neomodel import DoesNotExist, clear_neo4j_database, config, db

from app.helpers import NeomodelAwareJsonEncoder, get_env, items_per_page
from app.models import Course, KnowledgeArea, Topic, relationship_levels
from app.tests.helpers import (client_get, create_and_login_test_superuser,
                               create_and_login_test_user, create_courses,
                               create_knowledge_areas, create_topics, set_up)


class TopicViewsTestCase(InertiaTestCase):
    def setUp(self):
        set_up(InertiaTestCase, self)

    def test_topics_list_has_correct_props(self):
        create_and_login_test_user(self)
        create_knowledge_areas(5)
        create_courses(7)
        create_topics(3)

        props = client_get(self, reverse("app:topics.list"))

        self.assertComponentUsed("Topic/Form")

        self.assertEquals(len(props["initialTopics"]), 3)
        self.assertEquals(len(props["allCourses"]), 7)
        self.assertEquals(len(props["allKnowledgeAreas"]), 5)
        self.assertEquals(props["filter"], "")
        self.assertEquals(props["levels"], list(relationship_levels.values()))
        self.assertTrue(props["pageObj"])

    def test_topics_list_is_ordered_by_title(self):
        create_and_login_test_user(self)

        Topic(title="bor").save()
        Topic(title="foo").save()
        Topic(title="baz").save()

        props = client_get(self, reverse("app:topics.list"))

        self.assertEquals(props["initialTopics"][0]["title"], "baz")
        self.assertEquals(props["initialTopics"][1]["title"], "bor")
        self.assertEquals(props["initialTopics"][2]["title"], "foo")

    def test_topics_list_can_be_filtered(self):
        create_and_login_test_user(self)

        Topic(title="rty").save()
        Topic(title="foo").save()
        Topic(title="baz").save()

        props = client_get(self, reverse("app:topics.list") + "?filter=rt")

        self.assertEquals(len(props["initialTopics"]), 1)
        self.assertEquals(props["initialTopics"][0]["title"], "rty")

    def test_topics_list_can_be_paginated(self):
        create_and_login_test_user(self)

        create_topics(13)

        props = client_get(self, reverse("app:topics.list") + "?page=2")

        self.assertEquals(len(props["initialTopics"]), 13 - items_per_page)
        self.assertTrue(props["pageObj"])

    def test_get_courses(self):
        topics = create_topics(2)
        topic = topics[0]

        courses = create_courses(3)

        for course in courses:
            course.teaches.connect(topic, {"level": relationship_levels["beginner"]})

        create_and_login_test_user(self)

        json_response = self.client.get(
            reverse("app:topics.get_courses", args=[topic.uid])
        ).json()

        self.assertEquals(len(json_response), 3)

        json_response = self.client.get(
            reverse("app:topics.get_courses", args=[topics[1].uid])
        ).json()

        self.assertEquals(len(json_response), 0)

    def test_get_knowledge_areas(self):
        topics = create_topics(2)
        topic = topics[0]

        knowledge_areas = create_knowledge_areas(5)

        for knowledge_area in knowledge_areas:
            topic.covers.connect(
                knowledge_area, {"level": relationship_levels["beginner"]}
            )

        create_and_login_test_user(self)

        json_response = self.client.get(
            reverse("app:topics.get_knowledge_areas", args=[topic.uid])
        ).json()

        self.assertEquals(len(json_response), 5)

        json_response = self.client.get(
            reverse("app:topics.get_knowledge_areas", args=[topics[1].uid])
        ).json()

        self.assertEquals(len(json_response), 0)

    def test_create_topic_validation(self):
        create_and_login_test_user(self, client="inertia")

        response = self.inertia.post(
            reverse("app:topics.store"),
            json.dumps({"title": None}),
            content_type="application/json",
        )
        self.assertEquals(
            response.client.session["errors"],
            {"title": ["is required"]},
        )

        Topic(title="foo").save()
        response = self.inertia.post(
            reverse("app:topics.store"),
            json.dumps({"title": "foo"}),
            content_type="application/json",
        )
        self.assertEquals(
            response.client.session["errors"],
            {"title": ["must be unique"]},
        )

    def test_create_topic(self):
        create_and_login_test_user(self, client="inertia")

        self.inertia.post(
            reverse("app:topics.store"),
            json.dumps({"title": "foo"}),
            content_type="application/json",
        )

        topics = Topic.nodes.all()

        self.assertEquals(len(topics), 1)
        self.assertEquals(topics[0].title, "foo")

    def test_update_topic_validation(self):
        create_and_login_test_user(self, client="inertia")

        topics = create_topics(3)

        response = self.inertia.post(
            reverse("app:topics.update", args=[topics[0].uid]),
            json.dumps({"title": None}),
            content_type="application/json",
        )
        self.assertEquals(
            response.client.session["errors"],
            {"title": ["is required"]},
        )

    def test_update_topic(self):
        create_and_login_test_user(self, client="inertia")

        topic = create_topics(3)[0]

        self.inertia.post(
            reverse("app:topics.update", args=[topic.uid]),
            json.dumps({"title": "foo"}),
            content_type="application/json",
        )

        topic = Topic.nodes.get(uid=topic.uid)

        self.assertEquals(topic.title, "foo")

    def test_delete_topic(self):
        create_and_login_test_user(self, client="inertia")

        topic = create_topics(3)[0]

        self.inertia.post(
            reverse("app:topics.destroy", args=[topic.uid]),
            content_type="application/json",
        )

        with self.assertRaises(DoesNotExist):
            Topic.nodes.get(uid=topic.uid)

        self.assertEquals(len(Topic.nodes.all()), 2)
