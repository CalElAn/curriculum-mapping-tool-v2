from django.views.decorators.http import (require_GET)
from inertia import inertia

from app.cypher_queries import get_nodes_with_relationships
from app.models import (Course, Covers, IsPrerequisiteOf, KnowledgeArea,
                        Teaches, Topic, relationship_levels)


@inertia("Graph")
@require_GET
def view_graph(request):
    courses_teaches_topics = get_nodes_with_relationships(Course, Teaches, Topic)

    courses = [i["Course"] for i in courses_teaches_topics]

    topics_covers_knowledge_areas = get_nodes_with_relationships(
        Topic, Covers, KnowledgeArea
    )

    knowledge_areas = [i["KnowledgeArea"] for i in topics_covers_knowledge_areas]

    return {
        "courses": list(
            {getattr(course, "uid"): course for course in courses}.values()
        ),
        "topics": Topic.nodes.all(),
        "coursesWithTopics": courses_teaches_topics,
        "knowledgeAreas": list(
            {
                getattr(knowledge_area, "uid"): knowledge_area
                for knowledge_area in knowledge_areas
            }.values()
        ),
        "knowledgeAreasWithTopics": topics_covers_knowledge_areas,
        "prerequisiteCourses": get_nodes_with_relationships(
            Course, IsPrerequisiteOf, Course
        ),
        "levels": list(relationship_levels.values()),
    }
