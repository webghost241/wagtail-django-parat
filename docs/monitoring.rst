 .. _monitoring:

Monitoring
==========

Introduction
------------

Health routes are provided by ``django-health-check`` and rather than exposing a custom solution, parat uses its
default implementation.

Routes
^^^^^^

There is a single health route for the entire system, i.e. if your project provides an API, it does not feature a dedicate route for API
health checks (convention over configuration). The health route will return status ``200`` if the application is healthy and status code
``500`` if it is not. Both, the HTML as well as the JSON rendering contain information on which components are healthy and which aren't.

+--------+---------------------+-----------------------------------------------------------------------------------------+
| Method |        Route        |                                       Description                                       |
+========+=====================+=========================================================================================+
| GET    | /health/            | HTML rendering of health status                                                         |
+--------+---------------------+-----------------------------------------------------------------------------------------+
| GET    | /health/format=json | JSON rendering of health status, alternatively ``Accept: application/json`` can be used |
+--------+---------------------+-----------------------------------------------------------------------------------------+

Configured Checks
^^^^^^^^^^^^^^^^^

By default, the health checks cover: database, cache backend, storage, memory as well as migration checks. ``django-health-check`` supports
a variety of other checks via plugins, such as RabbitMQ, Redis and Celery.

Docker Compose
^^^^^^^^^^^^^^

By default, the Docker Compose health check is configured to probe the Django server periodically. This mechanism is used to automatically
restart Django during development.
