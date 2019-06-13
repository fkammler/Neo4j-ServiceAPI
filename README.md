# DataDrivenServiceAPI

This repository provides a code example of how business processes can be extended by sensor information and stored in the Neo4j graph database. The example contains a Python-based REST API that can be used to retrieve service activities and processes as JSON tuples from the graph.

We use the REST-API as a base structure for different prototypes based on it:

- A context-adaptive Augmented Reality Assistance System for Technical Customer Services in Mechanical Engineering
- A web-based orchestration tool for Smart Service Systems
- A general data storage for information exchange in product service systems

## Dependencies

The project can be instantiated and tested in just a few steps. Required is a running installation of the Neo4j graph database (tested with version 3.0.3), as well as the python3 libraries neo4j and bottle.

## Installation

Edit web_api_example.py according to your neo4j setup and you are ready to start:

```python
settings = {
    'user': 'neo4j',
    'password': 'example',
    'ip': '127.0.0.1',
    'port': 7687
}
```

## REST-Routes

##### /getStartByName/<name>
    
*Return start event for a given Name.*
    
 **Parameters:** name: String

 **Returns:** Dictionary as a representation of the start event
    
##### /getNodeById/<id>

* Return node for a given ID *

** Parameters: ** id: int

** Returns: ** Dictionary as a representation of the selected node

### /getNextById/<id>

* Return all next nodes for a given ID *
    
** Parameters: ** id: int

** Returns: ** Key 'nodes' is a list of dictionaries representing the successor nodes.

### /getStuffById/<id>/<stuff_type>
    
* Return attached stuff like tools or spareparts to a node given by ID *   
    
** Parameters: ** id: int
    
** Returns: ** Key 'stuff' is a lsit of dictionaries representing all attached stuff.

### /traverseTreeById/<id>

* Traverse process model starting from a node given by id and return a graph representation. *

** Parameters: ** id: int

** Returns: ** Dictionary as a representation of the graph. Keys are nodes (List of all nodes as dictionaries) and rels (list of all relationships as dictionaries)

### /getAllStuffById/<id>/<stuff_type>
    
* Return all attached stuff at the node given by id or at any successor node in the process model. *
    
** Parameters: ** id: int, stuff_type: string (optional)

** Returns: ** Key 'Stuff' has a list of all attachments as dictionaries

## Contribute

Contributions and extensions as well as application examples are very welcome. Please do not hesitate to contact us.

### Note:
- The repository also provides an exemplary business process ('cooling_error.cql') that can be used to test the database. To store the process in the database, you must simply query neo4j via its web interface with the entire code.
- In its current version, the code contains only rudimentary error handling.
