## General info
This repository is the main API of the Places Re-ranking applictaion, it takes the web clients requests and sends them to the ml ranking API, and finally returns the re-ranked places to the web clients.

## Code flow
* accept get requests from the web clients side (userlocations and places names in the request payload)
* extract user location and query from request
* send the users queries as search requests to Elasticsearch
* extract top 5 results returned from Elasticsearch
* send post request to the machine learning micro-service which re-ranks the Elasticsearch results (elasticsearch results as json in payload)
* send machine learning micro-service response to web client as a json 

## How to use

#### to build the docker image:

- run the command `docker build -t placeRankingManager:latest`
  - the `-t` is used to set the a TAG for the docker image

#### to run the service without the docker:

- run the command `python query_manager.py`

#### to use the service:

- send a GET request to the service containing the user location and the query (place name)
- example of the passed data:
```javascript
    { 
      "query" : "starbucks",
      "lat" : 40.224,
      "lon" : -70.345
    }
```

