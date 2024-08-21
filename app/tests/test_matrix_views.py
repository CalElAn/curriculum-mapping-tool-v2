from django.urls import reverse
from inertia.test import InertiaTestCase

from app.models import (relationship_levels)
from app.tests.helpers import (client_get, create_and_login_test_user, create_courses,
                               create_knowledge_areas, create_topics, set_up)


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