import json

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings, Client
from inertia.test import InertiaTestCase

from app.cypher_queries import get_nodes_with_relationships
from app.helpers import get_env, items_per_page, NeomodelAwareJsonEncoder
from django.urls import reverse
from neomodel import db, config, clear_neo4j_database, DoesNotExist

from app.models import (
    relationship_levels,
    Course,
    KnowledgeArea,
    Topic,
    Covers,
    Teaches,
)
from app.tests.helpers import (
    create_and_login_test_user,
    create_courses,
    create_topics,
    client_get,
    create_and_login_test_superuser,
    set_up,
    create_knowledge_areas,
)


class GraphViewsTestCase(InertiaTestCase):
    def setUp(self):
        set_up(InertiaTestCase, self)

    def test_view_graph_has_correct_props(self):
        create_and_login_test_user(self)

        courses = create_courses(8)
        topics = create_topics(7)
        knowledge_areas = create_knowledge_areas(4)

        for i in range(3):
            courses[i].teaches.connect(
                topics[i], {"level": relationship_levels["beginner"]}
            )

        for i in range(2):
            topics[i].covers.connect(
                knowledge_areas[i], {"level": relationship_levels["beginner"]}
            )

        courses[0].is_prerequisite_of.connect(courses[1])

        props = client_get(self, reverse("app:graph"))

        self.assertComponentUsed("Graph")

        self.assertEquals(len(props["courses"]), 3)
        self.assertEquals(len(props["topics"]), 7)
        self.assertEquals(len(props["coursesWithTopics"]), 3)
        self.assertEquals(len(props["knowledgeAreas"]), 2)
        self.assertEquals(len(props["knowledgeAreasWithTopics"]), 2)
        self.assertEquals(len(props["prerequisiteCourses"]), 1)
        self.assertEquals(props["levels"], list(relationship_levels.values()))
