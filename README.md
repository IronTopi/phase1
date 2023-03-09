# phase1

A small example of a RESTful CRUD-application, served as http-API.

Lets you read, insert, update and delete entries containing

- City name
- Start date
- and some more, see [Data](#data)

## Installing/Getting started

### Requirements

You need to be able to run `docker`/`docker compose` on your machine.

### Starting and stopping the system

If you're running this application on a linux host you can use the provided convenience scripts.
**First make sure the script-files are executable (`chmod a+x ./start.sh` etc.).**
If you want to eliminate all possible permission-related troubles just do a reckless `chmod -R 777 ./phase1`.

| script        | action                                                              |
| ------------- | ------------------------------------------------------------------- |
| `start.sh`    | starts all services, builds images if necessary                     |
| `stop.sh`     | stops the services                                                  |
| `clean_up.sh` | stops the services, removes images and persisted data from database |

If you don't run this on linux, just take a look inside the scripts and execute the commands manually.

### Connecting

The API will be served on Port `8080` of the host.
All endpoints are located under the `/items/`-route.

A detailed interactive documentation-UI for the API will be served under `:8080/docs`.
This does also provide the [openapi](https://www.openapis.org/)-style API-description (json-file).

The **default credentials** (set in `.env`) are:

- User: `dogbert`
- Password: `catbert`

### Data

Items look like following example:

```json
{
  "id": 59,
  "city": "Diwopu",
  "start_date": "2/20/2015",
  "end_date": "12/12/2014",
  "price": "81.90",
  "status": "Daily",
  "color": "#08c51b"
}
```

A set of 1000 items will be seeded into the database on the first startup of the application.

## Developing


### Built with
The following technologies are being used:

- http-API: [FastAPI](https://fastapi.tiangolo.com/)
- Data validation: [Pydantic](https://docs.pydantic.dev/)
- Database: [MongoDB](https://www.mongodb.com/)
- Containerization: 🐳 [docker](https://www.docker.com/)
- IDE: [VSCode](https://code.visualstudio.com/) with [Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers)

### Versions of base images

The version of the MongoDB is pinned in the `.env` file.
The **seeder** and **backend**-services have their python-version defined in their respective `Dockerfile`s.

### Logs

Logs are written to the `stdout` of the containers.
**FastAPI** logs all http-requests.
Errors from within the business layer are also logged (e.g. validation errors on malformed data).

```
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
ERROR:root:1 validation error for Item
start_date
  start_date '1114/13/2013' is not of format 'MM/DD/YYYY' (type=value_error)
INFO:     192.168.0.80:59193 - "GET /items/ HTTP/1.1" 200 OK
INFO:     192.168.0.80:59200 - "GET /items/100 HTTP/1.1" 200 OK
INFO:     192.168.0.80:59206 - "PUT /items/100 HTTP/1.1" 200 OK
INFO:     192.168.0.80:59209 - "DELETE /items/100 HTTP/1.1" 200 OK
ERROR:root:1 validation error for Item
start_date
  start_date '1114/13/2013' is not of format 'MM/DD/YYYY' (type=value_error)
INFO:     192.168.0.80:59314 - "GET /items/1 HTTP/1.1" 500 Internal Server Error
```

### Testing

Tests for the **backend**-service (mostly integration tests) are located in the folder `backend/src/test`.
To run the tests start the whole application and connect to the backend-service with a [VSCode Dev Container](https://code.visualstudio.com/docs/devcontainers/containers).
This will install the required python-modules and let you run `pytest --cov` from the workspace-folder (`/app` inside the dev-container):

```
============================= test session starts ==============================
platform linux -- Python 3.11.2, pytest-7.2.2, pluggy-1.0.0
rootdir: /app
plugins: cov-4.0.0, anyio-3.6.2
collected 20 items

test/Item_test.py ...........                                            [ 55%]
test/auth_test.py ..                                                     [ 65%]
test/backend_http_integration_test.py .......                            [100%]

---------- coverage: platform linux, python 3.11.2-final-0 -----------
Name                                    Stmts   Miss  Cover
-----------------------------------------------------------
api/models/Item.py                         37      0   100%
auth.py                                    15      0   100%
backend_http.py                            52      4    92%
dataaccess/IDatabaseConnection.py          22      6    73%
dataaccess/ItemDataRepository.py           43      4    91%
dataaccess/MongoDatabaseConnection.py      47      0   100%
test/Item_test.py                          21      0   100%
test/auth_test.py                          16      0   100%
test/backend_http_integration_test.py      63      3    95%
test/backend_http_test.py                   0      0   100%
-----------------------------------------------------------
TOTAL                                     316     17    95%


============================== 20 passed in 0.51s ==============================
```

## Things that have not been done

- API-Versioning (URL-versioning like `myapi/v1/`, see [FastAPI routers](https://fastapi.tiangolo.com/tutorial/bigger-applications/))
- SSL, rate-limiting (maybe offload to API-Gateway like [Kong](https://konghq.com/))
- Proper logging (implement log aggregation: let something like loki read your stdout/stderr and dump it into a centralized database, setup a nice dashboard or go full ELK-stack)
- Bake application into images instead of mounting the folders at runtime (in CI-pipeline)
- Automate tests in CI-pipeline
- Include type checking (mypy)
