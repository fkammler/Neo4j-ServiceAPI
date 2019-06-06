from neo4jprocess.neo4j_wrapper import Neo4jWrapper
import bottle

class Neo4jWebAPI:
    '''Wrapper around Neo4jWrapper to serve as a Web API.'''

    def __init__(self, settings):
        '''Construct a Neo4jWrapper Web API.

        Parameters
        ----------
        settings : dictionary
            Settings for the neo4j connection. Needs to specify following keys:
                - user
                - password
                - ip : use 127.0.0.1 for localhost
                - port
        '''

        self.proc = Neo4jWrapper(settings)

        # connect routes
        bottle.route("/getStartByName/<name>")(self.proc.get_start_by_name)
        bottle.route("/getNodeById/<id>")(self.proc.get_node_by_id)
        bottle.route("/getNextById/<id>")(self.proc.get_next_by_id)
        bottle.route("/getStuffById/<id>")(self.proc.get_stuff_by_id)
        bottle.route("/getStuffById/<id>/<stuff_type>")(self.proc.get_stuff_by_id)
        bottle.route("/traverseTreeById/<id>")(self.proc.traverse_tree_by_id)
        bottle.route("/getAllStuffById/<id>")(self.proc.get_all_stuff_by_id)
        bottle.route("/getAllStuffById/<id>/<stuff_type>")(self.proc.get_all_stuff_by_id)

    def run(self, host, port):
        '''Start the webserver.

        Parameters
        ----------
        host: string
            Hostname, probably 'localhost'.
        port: int
            Port to use.
        '''

        bottle.run(host=host, port=port)



if __name__ == '__main__':

    settings = {
        'user': 'neo4j',
        'password': 'star123',
        'ip': '127.0.0.1',
        'port': 7687
    }
    webapi = Neo4jWebAPI(settings)
    webapi.run(host='localhost', port=8080)
