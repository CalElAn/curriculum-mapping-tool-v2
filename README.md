# Curriculum Mapping Tool

<img width="975" height="496" alt="image" src="https://github.com/user-attachments/assets/c781a7a6-b075-472c-93a6-03fd3b9c3fc3" />

<img width="975" height="500" alt="image" src="https://github.com/user-attachments/assets/265bd272-f8cb-4913-be00-8d62119d9f5c" />


## Introduction
Curriculum mapping is the process of associating course-level learning outcomes with program-level learning outcomes. It is a practice routinely used by curriculum developers and reviewers to ensure that curricula are structured and organized strategically to meet program goals. This project will make use of a graph schema to organize curriculum data. Graph databases offer lots of flexibility in modelling complex structured and unstructured relationships between topics, courses and learning outcomes. Following the design of the scheme, curriculum data will be collected and stored in a graph database for subsequent retrieval and analysis. Graph visualizations and reporting tools will also be developed so that users can easily interact with and explore the data.

## Features

### Curriculum data model (Neo4j graph)
- **Three node types** modelled with `neomodel`: `Course` (number, title, code), `Topic` (title) and `KnowledgeArea` (title, description).
- **Three relationship types** between nodes:
  - `TEACHES` — connects a `Course` to a `Topic`, with `level`, `tools` and `comments` properties.
  - `COVERS` — connects a `Topic` to a `KnowledgeArea`, with `level`, `tools` and `comments` properties.
  - `IS_PREREQUISITE_OF` — connects a `Course` to another `Course`.
- **Relationship levels** of `beginner`, `intermediate` and `advanced` to capture depth of coverage.
- **Automatic UUIDs** and `created_at` / `updated_at` timestamps on every node and relationship.

### Data entry
- **Full CRUD** for Courses, Topics and Knowledge Areas via dedicated data-entry pages (`/data-entry/courses/`, `/data-entry/topics/`, `/data-entry/knowledge-areas/`).
- **Relationship subforms** to attach/detach Topics to Courses (`TEACHES`) and Knowledge Areas to Topics (`COVERS`) with level/tools/comments, directly from each node's row.
- **Inline search** by title or course number on every data-entry list.
- **Server-side pagination** with a reusable page navigation component.
- **Validation** using `django_rulebase` (required/integer/string rules) plus uniqueness checks (e.g. course number must be unique) — errors surface inline on the form.

### Graph visualization (`/graph/`)
- **Interactive force-directed graph** rendered with [vis-network](https://visjs.github.io/vis-network/docs/network/), showing courses, topics, knowledge areas and their relationships side-by-side.
- **Filter by course**: per-course checkboxes plus a "select all" toggle to hide/show nodes.
- **Filter by relationship type**: independently toggle `Prerequisites`, `Teaches` and `Covers` edges.
- **Edge weighting** by relationship level — higher levels render as thicker edges.
- **Hover tooltips** on nodes (course number/title, topic title, knowledge area title/description) and edges (level, tools, comments).
- **Truncated labels** for long topic/knowledge-area titles to keep the canvas readable.

### Matrix views
- **Courses × Topics matrix** (`/matrix/courses-and-topics`) showing the `TEACHES` level for every course/topic pair.
- **Topics × Knowledge Areas matrix** (`/matrix/topics-and-knowledge-areas`) showing the `COVERS` level for every topic/knowledge-area pair.
- **Rich cell tooltips** exposing the relationship's level, tools and comments.

### Authentication & authorization
- **Username/password login** via Django's built-in auth views, plus a self-service **sign-up** page (`/accounts/signup/`).
- **Login-required middleware** that gates every app route behind authentication.
- **Superuser-only middleware** that restricts create/update/delete operations on Courses and Knowledge Areas to admin users, while still allowing regular users to read and to manage Topics and relationships.
- **Django admin site** (`/admin/`) for low-level user and permissions management.

### Frontend experience
- **Vue 3 + TypeScript SPA** wired to Django through [Inertia.js](https://inertiajs.com/) — no separate API layer required.
- **Tailwind CSS** styling with reusable components (breadcrumbs, pagination, pill filters, sub-form wrappers, validation error blocks, SweetAlert dialogs, loading spinners).
- **Hot-module reload dev experience** through Vite + `django-vite`.

### Database seeding
- **Jupyter notebook seeder** (`neo4j_db_seeder/seeder.ipynb`) that loads an Excel/CSV export of curriculum links and bulk-creates courses, topics, knowledge areas and their relationships in Neo4j.

### Deployment & operations
- **Dockerized** for both development (`docker-compose.yml`) and production (`docker-compose.prod.yml` + `Dockerfile.prod`).
- **Nginx reverse-proxy config** and a `server_deploy.sh` helper for server provisioning.
- **Polyglot persistence**: Neo4j for the curriculum graph, MySQL for Django auth/sessions/admin data.

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

## Backend
- [Django](https://www.djangoproject.com/)

## Database
- [Neo4j](https://neo4j.com/)
- [neomodel](https://github.com/neo4j-contrib/neomodel)
- MySQL

Graph nodes and relationships are defined in `app/models.py`

## Seeding the Neo4j database
Open seeder.ipynb located in neo4j_db_seeder. 

Edit the password and username in the last but one cell. 

Run all the cells. 

You might want to comment this line `driver.execute_query(create_knowledge_areas_query, database_="neo4j")` in a production environment

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

## Contributing
Contributions are welcome! To contribute, follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## Support
For any questions or feedback, feel free to contact

## ToDo
1. Tests for helpers, middleware and cypher queries
2. Text search for the graph
