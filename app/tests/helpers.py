from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from faker import Faker
from inertia.test import InertiaTestCase
from neomodel import config, db

from app.helpers import get_env
from app.models import Course, KnowledgeArea, Topic

fake = Faker()


def set_up(inertia_test_case: type[InertiaTestCase], test_case: InertiaTestCase):
    inertia_test_case.setUp(test_case)
    config.DATABASE_URL = settings.TEST_NEOMODEL_NEO4J_BOLT_URL
    # print('ALL ITEMS IN DB ===',db.cypher_query('MATCH (n) RETURN n'))
    db.cypher_query("MATCH (n) DETACH DELETE n")


def client_get(test_case_instance: InertiaTestCase | TestCase, url: str) -> any:
    test_case_instance.client.get(url)

    return test_case_instance.props()


def create_and_login_test_user(
    test_case_instance: InertiaTestCase | TestCase, client="client"
):
    User.objects.create_user(username="test user", password="12345")

    getattr(test_case_instance, client).login(
        username="test user", password="12345"
    )


def create_and_login_test_superuser(
    test_case_instance: InertiaTestCase | TestCase, client="client"
):
    User.objects.create_superuser(username="test superuser", password="12345")

    getattr(test_case_instance, client).login(
        username="test superuser", password="12345"
    )


def create_courses(number_to_create: int) -> list[Course]:
    course_titles = fake.words(nb=number_to_create)

    courses = []

    for i, course_title in enumerate(course_titles):
        course = Course(title=course_title, number=i).save()
        courses.append(course)

    return courses


def create_topics(number_to_create: int) -> list[Topic]:
    topic_titles = fake.words(nb=number_to_create)

    topics = []

    for i, topic_title in enumerate(topic_titles):
        topic = Topic(title=topic_title).save()
        topics.append(topic)

    return topics


def create_knowledge_areas(number_to_create: int) -> list[KnowledgeArea]:
    titles = fake.words(nb=number_to_create)
    descriptions = fake.paragraphs(nb=number_to_create)

    knowledge_areas = []

    for i, title in enumerate(titles):
        course = KnowledgeArea(title=title, description=descriptions[i]).save()
        knowledge_areas.append(course)

    return knowledge_areas
