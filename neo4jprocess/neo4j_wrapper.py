from neo4j import GraphDatabase, basic_auth
from json import dumps

class Neo4jWrapper:
    '''This class provides an interface for acessing process models stored in a
    Neo4j graph-database as JSON.'''


    def __init__(self, settings):
        '''Construct a Neo4jWrapper.

        Parameters
        ----------
        settings : dictionary
            Settings for the neo4j connection. Needs to specify following keys:
                - user
                - password
                - ip : use 127.0.0.1 for localhost
                - port
        '''

        self.processor = QueryProcessor(settings)

    def get_start_by_name(self, name):
        '''Return start event for a given Name.

        Parameters
        ----------
        name : string
            The name of the start event.

        Returns
        -------
        dictionary
            Representation of the start event.
        '''

        query = """
            MATCH (a:Event {type:'start', name:{name}})
            RETURN a
        """
        parameters = {
            'name': name
        }
        return dumps(self.processor.get_node_json(query, parameters), indent=4, sort_keys=False, default=str)


    def get_node_by_id(self, id):
        '''Return node for a given id.

        Parameters
        ----------
        id : int or string
            The id of the node.

        Returns
        -------
        dictionary
            Representation of the node.
        '''

        query = """
            MATCH (a)
            WHERE ID(a)={id}
            RETURN a
        """
        parameters = {
            'id': int(id)
        }
        return dumps(self.processor.get_node_json(query, parameters), indent=4, sort_keys=False, default=str)

    def get_next_by_id(self, id):
        '''Return all next nodes for a given node id.

        Parameters
        ----------
        id : int or string
            The id of the given node.

        Returns
        -------
        dictionary
            Key 'nodes' is a list of dictionaries representing the successor
            nodes. Needs to be a dictionary and not a simple list to be JSON
            compliant.
        '''

        query = """
            MATCH (a)-[:SEQ]->(b)
            WHERE ID(a)={id}
            RETURN b
        """
        parameters = {
            'id': int(id)
        }
        return dumps(self.processor.get_node_list_json(query, parameters), indent=4, sort_keys=False, default=str)


    def get_next(self, current_node):
        '''Convenience wrapper around :meth:`Neo4jWrapper.get_next_by_id` for
        calling with a node.

        Parameters
        ----------
        current_node : dictionary
            Representation of the current node.

        Returns
        -------
        dictionary
            See :meth:`Neo4jWrapper.get_next_by_id`.
        '''

        return self.get_next_by_id(current_node['id'])


    def get_stuff_by_id(self, id, stuff_type=None):
        '''Return attached stuff like tools or spareparts to a node given by id.

        Parameters
        ----------
        id : int or string
            The id of the given node.
        stuff_type : string, optional
            If specified, only attachments of the given type are returned.

        Returns
        -------
        dictionary
            Key 'stuff' is a list of dictionaries representing all attached
            stuff.
        '''

        # either get all stuff, or only stuff of specific type
        if stuff_type is None:
            query = """
                MATCH (a)-[r]-(b)
                WHERE ID(a)={id}
                AND TYPE(r)<>'SEQ'
                RETURN r, b
            """
            parameters = {
                'id': int(id)
            }
        else:
            query = """
                MATCH (a)-[r]-(b)
                WHERE ID(a)={id}
                AND {stuff_type} IN LABELS(b)
                RETURN r, b
            """
            parameters = {
                'id': int(id),
                'stuff_type': stuff_type
            }
        return dumps(self.processor.get_stuff_json(query, parameters), indent=4, sort_keys=False, default=str)


    def get_stuff(self, current_node, stuff_type=None):
        '''Convenience wrapper around :meth:`Neo4jWrapper.get_stuff_by_id` for
        calling with a node.

        Parameters
        ----------
        current_node : dictionary
            Representation of the current node.
        stuff_type
            See :meth:`Neo4jWrapper.get_stuff_by_id`.

        Returns
        -------
        dictionary
            See :meth:`Neo4jWrapper.get_stuff_by_id`.
        '''

        return self.get_stuff_by_id(current_node['id'], stuff_type)

    def traverse_tree_by_id(self, id):
        '''Traverse process model starting from a node given by id and return a
        graph representation.

        Parameters
        ----------
        id : int or string
            The node id to start traversal from.

        Returns
        -------
        dictionary
            A representation of the graph. Keys are:
                - nodes: a list of all nodes as dictionaries
                - rels: a list of all relationships as dictionaries
        '''

        query = """
            MATCH (a)-[rs*]->(b)
            WHERE ID(a)={id}
            UNWIND rs as rel
            WITH
                a + COLLECT(DISTINCT(b)) AS nodes,
                COLLECT(DISTINCT(rel)) as rels
            RETURN nodes, rels
        """
        parameters = {
            'id': int(id)
        }
        return self.processor.get_graph_json(query, parameters)


    def get_all_stuff_by_id(self, id, stuff_type=None):
        '''Return all attached stuff at the node given by id or at any successor
        node in the process model.

        Parameters
        ----------
        id : int or string
            The id of the node from which to start traversal.
        stuff_type : string, optional
            If specified, only attachments of the given type are returned.

        Returns
        -------
        dictionary
            Key 'stuff' has a list of all attachments as dictionaries.
        '''

        # either get all stuff, or only stuff of specific type
        if stuff_type is None:
            query = """
                MATCH (a)-[rs*]->(b)
                WHERE ID(a)={id}
                WITH
                    rs[LENGTH(rs) - 1] as stuff_r,
                    b
                WHERE TYPE(stuff_r)<>'SEQ'
                RETURN
                    stuff_r,
                    b
            """
            parameters = {
                'id': int(id)
            }
        else:
            query = """
                MATCH (a)-[rs*]->(b)
                WHERE ID(a)={id}
                AND {stuff_type} IN LABELS(b)
                WITH
                    rs[LENGTH(rs) - 1] as stuff_r,
                    b
                RETURN
                    stuff_r,
                    b
            """
            parameters = {
                'id': int(id),
                'stuff_type': stuff_type
            }
        return dumps(self.processor.get_stuff_json(query, parameters), indent=4, sort_keys=False, default=str)



    def get_all_stuff(self, current_node, stuff_type=None):
        '''Convenience wrapper around :meth:`Neo4jWrapper.get_all_stuff` for
        calling with a node.

        Parameters
        ----------
        current_node : dictionary
            Representation of the current node.
        stuff_type
            See :meth:`Neo4jWrapper.get_all_stuff`.

        Returns
        -------
        dictionary
            See :meth:`Neo4jWrapper.get_all_stuff`.
        '''
        return self.get_all_stuff_by_id(current_node['id'], stuff_type)


class QueryProcessor:
    '''This class provides a wrapper around the neo4j-driver python-API for
    accessing business process models stored in neo4j as JSON with external
    queries.'''

    def __init__(self, settings):
        '''Construct a QueryProcessor and connect to the Neo4j-Database.

        Parameters
        ----------
        settings : dictionary
            Settings for the neo4j connection. Needs to specify following keys:
                - user
                - password
                - ip : use 127.0.0.1 for localhost
                - port
        '''

        auth = basic_auth(
            user=settings['user'],
            password=settings['password']
        )
        url = "bolt://{ip}:{port}".format(**settings)
        self.driver = GraphDatabase.driver(url, auth=auth)

    def get_node_json(self, query, parameters):
        '''Return a node for given query and parameters.

        Parameters
        ----------
        query : string
            The cypher query to run on the database. The query should return
            a single node.
        parameters : dictionary
            The parameters to pass to the cypher query.

        Returns
        -------
        dictionary
            Representation of the node.
        '''

        with self.driver.session() as s:
            node = s.run(query, **parameters).single()[0]
            return QueryProcessor.node_to_jsonlike(node)

    def get_node_list_json(self, query, parameters):
        '''Return all  nodes for a given query and parameters.

        Parameters
        ----------
        query : string
            The cypher query to run on the database. The query should return a
            list of nodes.
        parameters : dictionary
            The parameters to pass to the cypher query.

        Returns
        -------
        dictionary
            The only key 'nodes' is a list of dictionaries representing the
            nodes.
        '''

        with self.driver.session() as s:
            records = s.run(query, **parameters).records()
            list_of_nodes = [
                QueryProcessor.node_to_jsonlike(record[0]) for record in records
            ]
            return {'nodes': list_of_nodes}

    def get_stuff_json(self, query, parameters):
        '''Return attached stuff like tools or spareparts from a given query and
        parameters.

        Parameters
        ----------
        query : string
            The cypher query to run on the database. The query should return a
            list of tuples (relationship, stuff) in order to extract
            relationship information as well.
        parameters : dictionary
            The parameters to pass to the cypher query.

        Returns
        -------
        dictionary
            The only key 'stuff' is a list of dictionaries representing all
            attached stuff.
        '''

        with self.driver.session() as s:
            records = s.run(query, **parameters).records()
        # collect and process results
        resultlist = []
        for record in records:
            r, stuff = record.values()
            data = QueryProcessor.node_to_jsonlike(stuff)
            # for spareparts, there is an amount stored in the relationship
            # (node independent) that we need to include in the Representation
            # TODO: allow for including arbitrary relationship attributes
            if 'Sparepart' in data['labels']:
                data.update({'amount': r['amount']})
            resultlist.append(data)
        # return list of stuff nodes wrapped in dictionary for json compliance
        return {'stuff': resultlist}

    def get_graph_json(self, query, parameters):
        '''Return a subgraph for given query and parameters.

        Parameters
        ----------
        query : string
            The cypher query to run on the database. The query should return a
            single tuple of nodes and relationships of the subgraph.
        parameters : dictionary
            The parameters to pass to the cypher query.

        Returns
        -------
        dictionary
            A representation of the graph. Keys are:
                - nodes: a list of all nodes as dictionaries
                - rels: a list of all relationships as dictionaries
        '''

        with self.driver.session() as s:
            result = s.run(query, **parameters).single()
        # extract nodes and relationships from query result
        nodes = [
            QueryProcessor.node_to_jsonlike(node, include_type=False)
            for node in result['nodes']
        ]
        rels = [
            QueryProcessor.rel_to_jsonlike(rel, include_type=False)
            for rel in result['rels']
        ]
        # wrap in graph dictionary
        graph = {
            'type': 'Graph',
            'nodes': nodes,
            'rels': rels
        }
        return graph


    ############################################################################
    # Static Helpers
    ############################################################################

    @staticmethod
    def node_to_jsonlike(neo4j_object, include_type=True):
        '''Transform neo4j node object into jsonlike dictionary.

        Parameters
        ----------
        neo4j_object : neo4j.v1.Node
            Neo4j node object to be encoded in jsonlike dictionary.
        include_type : bool
            Whether to additionally include the type (Node) in the dictionary.

        Returns
        -------
        dictionary
            Jsonlike dictionary representation of neo4j_object.
        '''

        d = {**neo4j_object.__dict__}
        if include_type:
            d['type'] = 'Node'
        # labels is a python set, which is not json compliant, convert to list

        d['_labels'] = list(d['_labels'])
        return d

    @staticmethod
    def rel_to_jsonlike(neo4j_object, include_type=True):
        '''Transform neo4j relationship object into jsonlike dictionary.

        Parameters
        ----------
        neo4j_object : neo4j.v1.Relationship
            Neo4j relationship object to be encoded in jsonlike dictionary.
        include_type : bool
            Whether to additionally include the type (Relationship) in the
            dictionary.

        Returns
        -------
        dictionary
            Jsonlike dictionary representation of neo4j_object.
        '''

        d = {**neo4j_object.__dict__}
        if include_type:
            d['type'] = 'Rel'
        return d
