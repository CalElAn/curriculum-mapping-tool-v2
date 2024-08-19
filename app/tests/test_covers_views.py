import json

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings, Client
from inertia.test import InertiaTestCase

from app.cypher_queries import get_nodes_with_relationships
from app.helpers import get_env, items_per_page, NeomodelAwareJsonEncoder
from django.urls import reverse
from neomodel import db, config, clear_neo4j_database, DoesNotExist

from app.models import relationship_levels, Course, KnowledgeArea, Topic, Covers
from app.tests.helpers import (
    create_and_login_test_user,
    create_courses,
    create_topics,
    client_get,
    create_and_login_test_superuser,
    set_up,
    create_knowledge_areas,
)


class CoversViewsTestCase(InertiaTestCase):
    def setUp(self):
        set_up(InertiaTestCase, self)

    def test_create_covers_validation(self):
        create_and_login_test_user(self, client="inertia")

        response = self.inertia.post(
            reverse("app:covers.store"),
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

        topic = Topic(title="bar").save()
        knowledge_area = KnowledgeArea(title="foo").save()
        topic.covers.connect(knowledge_area, {"level": relationship_levels["beginner"]})

        response = self.inertia.post(
            reverse("app:covers.store"),
            json.dumps(
                {
                    "knowledge_area_uid": knowledge_area.uid,
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

    def test_create_covers(self):
        create_and_login_test_user(self, client="inertia")

        topic = Topic(title="bar").save()
        knowledge_area = KnowledgeArea(title="foo").save()

        self.inertia.post(
            reverse("app:covers.store"),
            json.dumps(
                {
                    "knowledge_area_uid": knowledge_area.uid,
                    "topic_uid": topic.uid,
                    "level": relationship_levels["beginner"],
                    "tools": "foo",
                    "comments": "bar",
                }
            ),
            content_type="application/json",
        )

        topic_covers_knowledge_area = get_nodes_with_relationships(
            Topic, Covers, KnowledgeArea, Topic, topic.uid
        )
        covers = topic_covers_knowledge_area[0]["COVERS"]

        self.assertEquals(len(topic_covers_knowledge_area), 1)
        self.assertEquals(covers.level, relationship_levels["beginner"])
        self.assertEquals(covers.tools, "foo")
        self.assertEquals(covers.comments, "bar")

    def test_update_covers_validation(self):
        create_and_login_test_user(self, client="inertia")

        topic = Topic(title="bar").save()
        knowledge_area = KnowledgeArea(title="foo").save()
        topic.covers.connect(knowledge_area, {"level": relationship_levels["beginner"]})

        covers = get_nodes_with_relationships(
            Topic, Covers, KnowledgeArea, Topic, topic.uid
        )[0]["COVERS"]

        response = self.inertia.post(
            reverse("app:covers.update", args=[covers.uid]),
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

    def test_update_covers(self):
        create_and_login_test_user(self, client="inertia")

        topic = Topic(title="bar").save()
        knowledge_area = KnowledgeArea(title="foo").save()
        topic.covers.connect(
            knowledge_area,
            {
                "level": relationship_levels["beginner"],
                "tools": "tool 1",
                "comments": "comment 1",
            },
        )

        covers = get_nodes_with_relationships(
            Topic, Covers, KnowledgeArea, Topic, topic.uid
        )[0]["COVERS"]

        self.inertia.post(
            reverse("app:covers.update", args=[covers.uid]),
            json.dumps(
                {
                    "level": relationship_levels["intermediate"],
                    "tools": "tool 22",
                    "comments": "comment 22",
                }
            ),
            content_type="application/json",
        )

        covers = get_nodes_with_relationships(
            Topic, Covers, KnowledgeArea, Topic, topic.uid
        )[0]["COVERS"]

        self.assertEquals(covers.level, relationship_levels["intermediate"])
        self.assertEquals(covers.tools, "tool 22")
        self.assertEquals(covers.comments, "comment 22")

    def test_delete_covers(self):
        create_and_login_test_user(self, client="inertia")

        topic = Topic(title="bar").save()
        knowledge_area = KnowledgeArea(title="foo").save()
        topic.covers.connect(
            knowledge_area,
            {
                "level": relationship_levels["beginner"],
            },
        )

        covers = get_nodes_with_relationships(
            Topic, Covers, KnowledgeArea, Topic, topic.uid
        )[0]["COVERS"]

        self.inertia.post(
            reverse("app:covers.destroy", args=[covers.uid]),
            content_type="application/json",
        )

        topic_covers_knowledge_area = get_nodes_with_relationships(
            Topic, Covers, KnowledgeArea, Topic, topic.uid
        )

        self.assertEquals(len(topic_covers_knowledge_area), 0)
