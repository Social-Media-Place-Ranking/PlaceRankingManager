# PlaceRankingManeger

This repository is the backend of the Places Re-ranking applictaion, The prodecures involved in this code are as follows:
- accepting get request from the web client side (userlocation and query in the request payload)
- extract user location and query from request
- send the users query in a search request to elasticsearch
- extract top 5 results returned from elasticsearch
- send post request to machine learning micro-service which reranks the elasticsearch results (elasticsearch results as json in payload)
- send micro-service response to web client in json format 
