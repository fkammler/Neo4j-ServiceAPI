from neo4jprocess.neo4j_web_api  import Neo4jWebAPI

settings = {
    'user': 'neo4j',
    'password': 'example',
    'ip': '127.0.0.1',
    'port': 7687
}
webapi = Neo4jWebAPI(settings)
webapi.run(host='localhost', port=8080)
