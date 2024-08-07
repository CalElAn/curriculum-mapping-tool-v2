from typing import Type, Union

from neomodel import db, StructuredNode, StructuredRel


def get_nodes_with_relationships(
    from_node: Type[StructuredNode],
    relationship: Type[StructuredRel],
    to_node: Type[StructuredNode],
    node_to_find: Type[StructuredNode] = None,
    node_to_find_uid: str = None,
    order_by: str | None = None,
    node_to_order_by: Type[StructuredNode] | Type[StructuredNode] | None = None,
) -> list[dict[str, Union[Type[StructuredNode | StructuredRel]]]]:
    from_node_label = from_node.__label__
    from_node_var = from_node_label

    relationship_label = relationship.__label__

    to_node_label = to_node.__label__
    to_node_var = to_node_label

    if from_node_var == to_node_var:
        from_node_var = f"{from_node_var}_from"
        to_node_var = f"{to_node_var}_to"

    cypher_query = f"""
        MATCH ({from_node_var}:{from_node_label})-[{relationship_label}:{relationship_label}]->({to_node_var}:{to_node_label})    
        """

    if node_to_find and node_to_find_uid:
        cypher_query += f'WHERE {node_to_find.__label__}.uid = "{node_to_find_uid}"'

    cypher_query += f"RETURN {from_node_var}, {relationship_label}, {to_node_var}"

    if order_by and node_to_order_by:
        cypher_query += (
            f" ORDER BY LOWER(toString({node_to_order_by.__label__}.{order_by}))"
        )

    query_results, cols = db.cypher_query(cypher_query)

    results = []

    for row in query_results:
        results.append(
            {
                from_node_var: from_node.inflate(row[cols.index(from_node_var)]),
                relationship_label: relationship.inflate(
                    row[cols.index(relationship_label)]
                ),
                to_node_var: to_node.inflate(row[cols.index(to_node_var)]),
            }
        )

    return results


def get_relationship(
    relationship: Type[StructuredRel], uid: str
) -> Type[StructuredRel]:
    cypher_query = f"""
        MATCH ()-[r:{relationship.__label__}{{ uid: "{uid}" }}]->()
        RETURN r    
        """

    query_results, cols = db.cypher_query(cypher_query)

    return relationship.inflate(query_results[0][0])


def delete_relationship(relationship: Type[StructuredRel], uid: str):
    cypher_query = f"""
        MATCH ()-[r:{relationship.__label__}{{ uid: "{uid}" }}]->()
        DELETE r    
        """

    db.cypher_query(cypher_query)
