import json

from django.urls import reverse
from inertia.test import InertiaTestCase
from neomodel import DoesNotExist

from app.helpers import items_per_page
from app.models import KnowledgeArea, relationship_levels
from app.tests.helpers import (client_get, create_and_login_test_superuser,
                               create_and_login_test_user, create_knowledge_areas, create_topics, set_up)


class KnowledgeAreaViewsTestCase(InertiaTestCase):
    def setUp(self):
        set_up(InertiaTestCase, self)

    def test_knowledge_areas_list_has_correct_props(self):
        create_and_login_test_user(self)
        create_knowledge_areas(5)
        create_topics(3)

        props = client_get(self, reverse("app:knowledge_areas.list"))

        self.assertComponentUsed("KnowledgeArea/Form")

        self.assertEquals(len(props["initialKnowledgeAreas"]), 5)
        self.assertEquals(len(props["allTopics"]), 3)
        self.assertEquals(props["filter"], "")
        self.assertEquals(props["levels"], list(relationship_levels.values()))
        self.assertTrue(props["pageObj"])

    def test_knowledge_areas_list_is_ordered_by_title(self):
        create_and_login_test_user(self)

        KnowledgeArea(title="bor", description="qwe").save()
        KnowledgeArea(title="foo", description="uio").save()
        KnowledgeArea(title="baz", description="rty").save()

        props = client_get(self, reverse("app:knowledge_areas.list"))

        self.assertEquals(props["initialKnowledgeAreas"][0]["title"], "baz")
        self.assertEquals(props["initialKnowledgeAreas"][1]["title"], "bor")
        self.assertEquals(props["initialKnowledgeAreas"][2]["title"], "foo")

    def test_knowledge_areas_list_can_be_filtered(self):
        create_and_login_test_user(self)

        KnowledgeArea(title="rty", description="qwe").save()
        KnowledgeArea(title="foo", description="uio").save()
        KnowledgeArea(title="baz", description="party").save()

        props = client_get(self, reverse("app:knowledge_areas.list") + "?filter=rt")

        self.assertEquals(len(props["initialKnowledgeAreas"]), 2)
        self.assertEquals(props["initialKnowledgeAreas"][0]["description"], "party")
        self.assertEquals(props["initialKnowledgeAreas"][1]["title"], "rty")

    def test_knowledge_areas_list_can_be_paginated(self):
        create_and_login_test_user(self)

        create_knowledge_areas(13)

        props = client_get(self, reverse("app:knowledge_areas.list") + "?page=2")

        self.assertEquals(len(props["initialKnowledgeAreas"]), 13 - items_per_page)
        self.assertTrue(props["pageObj"])

    def test_get_topics(self):
        knowledge_areas = create_knowledge_areas(2)

        knowledge_area = knowledge_areas[0]

        topics = create_topics(3)

        for topic in topics:
            topic.covers.connect(
                knowledge_area, {"level": relationship_levels["beginner"]}
            )

        create_and_login_test_user(self)

        json_response = self.client.get(
            reverse("app:knowledge_areas.get_topics", args=[knowledge_area.uid])
        ).json()

        self.assertEquals(len(json_response), 3)

        json_response = self.client.get(
            reverse("app:knowledge_areas.get_topics", args=[knowledge_areas[1].uid])
        ).json()

        self.assertEquals(len(json_response), 0)

    def test_only_superusers_can_create_update_and_delete_knowledge_areas(self):
        create_and_login_test_user(self)

        response_json = self.client.post(
            reverse("app:knowledge_areas.store"),
            content_type="application/json",
        ).json()

        self.assertEquals(
            response_json, {"message": "This action can only be performed by an admin"}
        )

        for route in ("update", "destroy"):
            response_json = self.client.post(
                reverse(f"app:knowledge_areas.{route}", args=["foo"]),
                content_type="application/json",
            ).json()

            self.assertEquals(
                response_json,
                {"message": "This action can only be performed by an admin"},
            )

    def test_create_knowledge_area_validation(self):
        create_and_login_test_superuser(self, client="inertia")

        response = self.inertia.post(
            reverse("app:knowledge_areas.store"),
            json.dumps({"title": None, "description": None}),
            content_type="application/json",
        )
        self.assertEquals(
            response.client.session["errors"],
            {"title": ["is required"], "description": ["is required"]},
        )

    def test_create_knowledge_area(self):
        create_and_login_test_superuser(self, client="inertia")

        self.inertia.post(
            reverse("app:knowledge_areas.store"),
            json.dumps({"title": "foo", "description": "bar"}),
            content_type="application/json",
        )

        knowledge_areas = KnowledgeArea.nodes.all()

        self.assertEquals(len(knowledge_areas), 1)
        self.assertEquals(knowledge_areas[0].title, "foo")
        self.assertEquals(knowledge_areas[0].description, "bar")

    def test_update_knowledge_areas_validation(self):
        create_and_login_test_superuser(self, client="inertia")

        knowledge_areas = create_knowledge_areas(3)

        response = self.inertia.post(
            reverse("app:knowledge_areas.update", args=[knowledge_areas[0].uid]),
            json.dumps({"title": None, "description": None}),
            content_type="application/json",
        )
        self.assertEquals(
            response.client.session["errors"],
            {"title": ["is required"], "description": ["is required"]},
        )

    def test_update_knowledge_area(self):
        create_and_login_test_superuser(self, client="inertia")

        knowledge_area = create_knowledge_areas(3)[0]

        self.inertia.post(
            reverse("app:knowledge_areas.update", args=[knowledge_area.uid]),
            json.dumps({"title": "foo", "description": "bar"}),
            content_type="application/json",
        )

        knowledge_area = KnowledgeArea.nodes.get(uid=knowledge_area.uid)

        self.assertEquals(knowledge_area.title, "foo")
        self.assertEquals(knowledge_area.description, "bar")

    def test_delete_knowledge_area(self):
        create_and_login_test_superuser(self, client="inertia")

        knowledge_area = create_knowledge_areas(3)[0]

        self.inertia.post(
            reverse("app:knowledge_areas.destroy", args=[knowledge_area.uid]),
            content_type="application/json",
        )

        with self.assertRaises(DoesNotExist):
            KnowledgeArea.nodes.get(uid=knowledge_area.uid)

        self.assertEquals(len(KnowledgeArea.nodes.all()), 2)
