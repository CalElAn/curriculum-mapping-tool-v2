from uuid import uuid4

from django.db import models
from neomodel import (
    StructuredNode,
    StringProperty,
    DateTimeNeo4jFormatProperty,
    IntegerProperty,
    RelationshipTo,
    StructuredRel,
    ZeroOrMore,
    OneOrMore,
    ZeroOrOne,
)

relationship_levels = {
    "beginner": "beginner",
    "intermediate": "intermediate",
    "advanced": "advanced",
}


# Always define a __labels__ property for relationships

class TeachesRel(StructuredRel):
    __label__ = "TEACHES"
    uid = StringProperty(unique_index=True, default=uuid4)
    level = StringProperty(required=True, choices=relationship_levels)
    comments = StringProperty()
    created_at = DateTimeNeo4jFormatProperty()
    updated_at = DateTimeNeo4jFormatProperty()


class IsPrerequisiteOfRel(StructuredRel):
    __label__ = "IS_PREREQUISITE_OF"
    uid = StringProperty(unique_index=True, default=uuid4)


class CoversRel(StructuredRel):
    __label__ = "COVERS"
    uid = StringProperty(unique_index=True, default=uuid4)
    level = StringProperty(required=True, choices=relationship_levels)
    comments = StringProperty()
    created_at = DateTimeNeo4jFormatProperty()
    updated_at = DateTimeNeo4jFormatProperty()


class Course(StructuredNode):
    uid = StringProperty(unique_index=True, default=uuid4)
    number = IntegerProperty()
    title = StringProperty()
    code = StringProperty()
    teaches = RelationshipTo(
        "Topic", "TEACHES", cardinality=ZeroOrMore, model=TeachesRel
    )
    is_prerequisite_of = RelationshipTo(
        "Course",
        "IS_PREREQUISITE_OF",
        cardinality=ZeroOrMore,
        model=IsPrerequisiteOfRel,
    )
    created_at = DateTimeNeo4jFormatProperty(default_now=True)
    updated_at = DateTimeNeo4jFormatProperty(default_now=True)


class Topic(StructuredNode):
    uid = StringProperty(unique_index=True, default=uuid4)
    name = StringProperty(unique_index=True)
    covers = RelationshipTo(
        "KnowledgeArea", "COVERS", cardinality=ZeroOrOne, model=CoversRel
    )
    created_at = DateTimeNeo4jFormatProperty()
    updated_at = DateTimeNeo4jFormatProperty()


class KnowledgeArea(StructuredNode):
    uid = StringProperty(unique_index=True, default=uuid4)
    title = StringProperty()
    description = StringProperty()
    created_at = DateTimeNeo4jFormatProperty()
    updated_at = DateTimeNeo4jFormatProperty()
