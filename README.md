# Searchy

![CI-CD Status](https://github.com/oryan-omer/searchy/actions/workflows/main.yaml/badge.svg
)

[![Python Version](https://img.shields.io/badge/python-3.9-blue?logo=python&style=flat-square)](https://www.python.org/downloads/)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/f0171a2d51dc4b558ff00304344fd025)](https://app.codacy.com/gh/oryan-omer/searchy/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)  
[![SonarCloud](https://sonarcloud.io/images/project_badges/sonarcloud-white.svg)](https://sonarcloud.io/summary/new_code?id=oryan-omer_searchy)

Searchy is a powerful and flexible Python-based search engine that is built using a variety of technologies.  
It utilizes FastAPI as its web framework, which provides a high-performance and easy-to-use RESTful API for serving search requests.        
The search engine itself is built using Elasticsearch, a highly scalable and distributed search and analytics engine that is designed to handle large amounts of data.     
Finally, Searchy also uses Redis, an open-source, in-memory data structure store, to cache frequently accessed data and improve performance.  


## Requirements:
- Python 3.8 or higher
- Docker
- Docker Compose

## Installation

To install Searchy, clone the repository and navigate to the project directory:

```bash
git clone https://github.com/oryan-omer/searchy.git
cd searchy
```

Install the required dependencies using Poetry:

```bash
poetry install
```

## Running the App Locally
1. Start Elasticsearch and Redis using Docker Compose:
```python
docker-compose up -d elasticsearch redis
```
an alternative
```python
make run-dev
```


2. Run the app:
```bash
make run
```

3. The app should now be accessible at http://localhost:80.

## Running on top of K8S
Searchy can be deployed to a Kubernetes cluster using a Helm chart. The chart can be customized to fit your specific needs, including configuring Elasticsearch and Redis settings, scaling the number of replicas, and setting up ingress and other networking options. Once deployed, you can use the Searchy API to power your search application, or integrate it into other services as needed.

## Testing
To run the test suite, use the following command:

```bash
make test
```

## Contributing
Contributions to Searchy are welcome! If you would like to contribute, please submit a pull request and ensure that all tests pass.

## License
Searchy is licensed under the MIT License.