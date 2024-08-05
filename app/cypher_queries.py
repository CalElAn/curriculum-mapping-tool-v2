from typing import Type, Union

from neomodel import db, StructuredNode, StructuredRel


def get_nodes_with_relationships(
    from_node: Type[StructuredNode],
    relationship: Type[StructuredRel],
    to_node: Type[StructuredNode],
    node_to_find: Type[StructuredNode],
    node_to_find_uid: str,
    order_by: str | None = None,
    node_to_order_by: Type[StructuredNode] | Type[StructuredNode] | None = None,
) -> list[dict[str, Union[Type[StructuredNode | StructuredRel]]]]:
    from_node_label = from_node.__label__
    relationship_label = relationship.__label__
    to_node_label = to_node.__label__
    node_to_find_label = node_to_find.__label__
    node_to_order_by_label = node_to_order_by.__label__ if node_to_order_by else None

    cypher_query = f"""
        MATCH ({from_node_label}:{from_node_label})-[{relationship_label}:{relationship_label}]->({to_node_label}:{to_node_label})
        WHERE {node_to_find_label}.uid = "{node_to_find_uid}"
        RETURN {from_node_label}, {relationship_label}, {to_node_label}
        """

    if order_by and node_to_order_by:
        cypher_query += (
            f" ORDER BY LOWER(toString({node_to_order_by_label}.{order_by}))"
        )

    query_results, cols = db.cypher_query(cypher_query)

    results = []

    for row in query_results:
        results.append(
            {
                from_node_label: from_node.inflate(row[cols.index(from_node_label)]),
                relationship_label: relationship.inflate(
                    row[cols.index(relationship_label)]
                ),
                to_node_label: to_node.inflate(row[cols.index(to_node_label)]),
            }
        )

    return results
