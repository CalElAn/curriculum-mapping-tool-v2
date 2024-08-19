# Curriculum Mapping Tool

## Introduction
Curriculum mapping is the process of associating course-level learning outcomes with program-level learning outcomes. It is a practice routinely used by curriculum developers and reviewers to ensure that curricula are structured and organized strategically to meet program goals. This project will make use of a graph schema to organize curriculum data. Graph databases offer lots of flexibility in modelling complex structured and unstructured relationships between topics, courses and learning outcomes. Following the design of the scheme, curriculum data will be collected and stored in a graph database for subsequent retrieval and analysis. Graph visualizations and reporting tools will also be developed so that users can easily interact with and explore the data. 

## Prerequisites
- Docker

## Frontend
- [vue.js](https://vuejs.org/)
- [vite.js](https://vitejs.dev/)
- [django-vite](https://github.com/MrBin99/django-vite)
- [inertia](https://inertiajs.com/)
- [inertia-django](https://github.com/inertiajs/inertia-django)
- [tailwind css](https://tailwindcss.com/)

Frontend code is located in `static/app/src/`

## Database
- [Neo4j](https://neo4j.com/)
- [neomodel](https://github.com/neo4j-contrib/neomodel)
- MySQL

Graph nodes and relationships are defined in `app/models.py`

## Development
```
git clone https://github.com/CalElAn/curriculum-mapping-tool-v2.git
cd curriculum-mapping-tool-v2
cp env.example .env
```

Update the .env file with the appropriate configurations

`docker compose up`

Access the application by navigating to http://localhost:8000 in your web browser.

## Deployment
```
git clone https://github.com/CalElAn/curriculum-mapping-tool-v2.git
cd curriculum-mapping-tool-v2
cp env.example .env
```

Update the .env file with the appropriate configurations

`. server_deploy.sh`

You might want to go over the `server_deploy.sh` file before running it for the first time.

## Testing
To run tests, execute:

`docker compose exec python bash -c "python ./manage.py test app.tests"`

## Contact
For any questions or feedback, feel free to contact
