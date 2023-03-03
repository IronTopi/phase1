# ATTENTION:
# Container-names are explicitly prefixed in start.sh (docker compose -p)
# If the containers were not spun up via the start-script this here
# might not work (-> different image name!)
./stop.sh
source .env

# remove images
docker rmi $PROJECT_PREFIX-backend
docker rmi mongo:$MONGO_VERSION

# remove database volume
docker volume rm "$PROJECT_PREFIX"_database_persistence