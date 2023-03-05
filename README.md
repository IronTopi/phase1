# phase1

A minimalistic example of a RESTful CRUD-application.

Lets you read, insert, update and delete entries containing

- City name
- Start date
- and some more, see [Data](#data)

## Setup

### Requirements

You need to be able to run `docker`/`docker compose`

### Starting and stopping the system

If you're running this application on a linux host, you can use the provided convenience scripts.
**First make sure the script-files are executable (`chmod a+x ./start.sh` etc.).**

| script        | action                                                              |
| ------------- | ------------------------------------------------------------------- |
| `start.sh`    | starts all services, builds images if necessary                     |
| `stop.sh`     | stops the services                                                  |
| `clean_up.sh` | stops the services, removes images and persisted data from database |

## Connecting

The API will be served on Port `8080` of the host.
A simple UI will be served under `:8080/docs`.

The **default credentials** (set in `.env`) are:

- User: `dogbert`
- Password: `catbert`

## Data

TODO: Format as table

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

## Development and Tech

- http-API: [FastAPI](https://fastapi.tiangolo.com/)
- Data validation: [Pydantic](https://docs.pydantic.dev/)
- Database: [MongoDB](https://www.mongodb.com/)
- Containerization: 🐳 [docker](https://www.docker.com/)

TODO: small architecture diagram

### Versions

The version of the MongoDB can is pinned in the `.env` file.
The **seeder** and **backend**-services have their version defined in their respective `Dockerfile`s.

```[.env]
MONGO_VERSION=6.0.4
```

### Setting up Dev-Environment

### Testing

Tests for the **backend**-service (mostly integration test) are located in the folder `backend/src/test`.
To run the tests start the whole application (see open the backend-servie in

## Things that have not been done

- API-Versioning (maybe URL-versioning like `myapi/v1/`, see [FastAPI routers](https://fastapi.tiangolo.com/tutorial/bigger-applications/))
- SSL, rate-limiting (maybe offload to API-Gateway like [Kong](https://konghq.com/))
- Proper logging (larger systems implement log aggregation: let something like loki read your stdout/stderr)
