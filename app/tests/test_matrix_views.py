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

class MatrixViewsTestCase(InertiaTestCase):
    def setUp(self):
        set_up(InertiaTestCase, self)

    def test_view_courses_and_topics_matrix_has_correct_props(self):
        create_and_login_test_user(self)

        courses = create_courses(8)
        topics = create_topics(7)

        for i in range(3):
            courses[i].teaches.connect(
                topics[i], {"level": relationship_levels["beginner"]}
            )

        props = client_get(self, reverse("app:matrix.courses_and_topics"))

        self.assertComponentUsed("Matrix/CoursesAndTopics")

        self.assertEquals(len(props["courses"]), 8)
        self.assertEquals(len(props["topics"]), 7)
        self.assertEquals(len(props["coursesTeachesTopics"]), 3)

    def test_view_topics_and_knowledge_areas_matrix_has_correct_props(self):
        create_and_login_test_user(self)

        topics = create_topics(7)
        knowledge_areas = create_knowledge_areas(4)

        for i in range(2):
            topics[i].covers.connect(
                knowledge_areas[i], {"level": relationship_levels["beginner"]}
            )

        props = client_get(self, reverse("app:matrix.topics_and_knowledge_areas"))

        self.assertComponentUsed("Matrix/TopicsAndKnowledgeAreas")

        self.assertEquals(len(props["topics"]), 7)
        self.assertEquals(len(props["knowledgeAreas"]), 4)
        self.assertEquals(len(props["topicsCoversKnowledgeAreas"]), 2)