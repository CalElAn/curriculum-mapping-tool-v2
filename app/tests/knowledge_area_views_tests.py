import json

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings, Client
from inertia.test import InertiaTestCase
from app.helpers import get_env, items_per_page, NeomodelAwareJsonEncoder
from django.urls import reverse
from neomodel import db, config, clear_neo4j_database, DoesNotExist

from app.models import relationship_levels, Course, KnowledgeArea
from app.tests.helpers import (
    create_and_login_test_user,
    create_courses,
    create_topics,
    client_get,
    create_and_login_test_superuser,
    set_up,
)


class KnowledgeAreaViewsTestCase(InertiaTestCase):
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