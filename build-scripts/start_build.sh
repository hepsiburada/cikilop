#!/usr/bin/env sh

ClearEnvironment(){
    docker rmi -f $(docker images | grep '^<none>' | awk '{print $3}') || true
    docker rmi -f $(docker images | grep cikilop | awk '{print $3}') || true
    docker rm -f $(docker ps -a | grep cikilop_cikilop | awk '{print $1}') || true
}

ClearEnvironment

docker-compose up -d

if [ $? = 0 ]; then
  echo "Successfull build..."
  docker build --network="host" -t hepsiburada/cikilop:latest -t hepsiburada/cikilop:1.0.0 .
  # docker push hepsiburada/cikilop:1.0.0
  # docker push hepsiburada/cikilop:latest
  exit 0
else
  echo "Process failed..."
  exit 1
fi

docker-compose down
