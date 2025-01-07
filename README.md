Ecommerce Backend

NOTES: 
  - Running tests container with pytest-watch throws an error so the container uses pytest as a temporary solution
  - Since dev settings are hardcoded, a .env file is only necessary for prod

Stack:
  * Python
  * Django
  * Django Rest Framework
  * PostgresQL
  * Redis
  * Celery
  * Pytest
  * Locust
  * Silk

Description:
  * Image uploding 
  * Email sending
  * Running background tasks with Celery
  * Unit testing with Pytest
  * Performance testing with Locust
  * Profiling with Silk
  * Caching with Redis
  * Logging
  * Dev and prod settings

Steps to run:
  * Run "pipenv install" to install dependencies
  * Run "docker-compose up -d" file to start containers