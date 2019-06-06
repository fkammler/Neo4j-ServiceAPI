from neo4jprocess.neo4j_wrapper import Neo4jWrapper

settings = {
    'user': 'neo4j',
    'password': 'example',
    'ip': '127.0.0.1',
    'port': 7687
}

process = Neo4jWrapper(settings)

start = process.get_start_by_name('Machine burns')

print(start)
print("------")
print(process.get_node_by_id(start['id']))
print("------")
print(process.get_next_by_id(start['id']))
print("------")
print(process.get_next(start))
print("------")

a1 = process.get_next(start)['nodes'][0]

print(process.get_stuff_by_id(a1['id']))
print("------")
print(process.get_stuff(a1))
print("------")
print(process.get_all_stuff(a1))
print("------")
print(process.traverse_tree_by_id(a1['id']))
print("------")
