# DataDrivenServiceAPI

This repository provides a code example of how business processes can be extended by sensor information and stored in the Neo4j graph database. The example contains a Python-based REST API that can be used to retrieve service activities and processes as JSON tuples from the graph.

We use the REST-API as a base structure for different prototypes based on it:

- A context-adaptive Augmented Reality Assistance System for Technical Customer Services in Mechanical Engineering
- A web-based orchestration tool for Smart Service Systems
- A general data storage for information exchange in product service systems

## Installation

The project can be instantiated and tested in just a few steps. Required is a running installation of the Neo4j graph database (tested with version 3.0.3), as well as the python3 libraries neo4j and bottle.

Edit web_api_example.py according to your neo4j setup and you are ready to start:

```python
settings = {
    'user': 'neo4j',
    'password': 'example',
    'ip': '127.0.0.1',
    'port': 7687
}
´´´

## REST-Pipes



## Contribute

Note:
- The repository also provides an exemplary business process ('cooling_error.cql') that can be used to test the database. To store the process in the database, you must simply query neo4j via its web interface with the entire code.
- In its current version, the code contains only rudimentary error handling.
