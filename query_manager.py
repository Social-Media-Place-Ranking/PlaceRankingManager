"""
Import Necessary Libraries 
"""
from flask import Flask, request, jsonify, json
from elasticsearch import Elasticsearch
import requests
import os

app = Flask(__name__)

"""
Flask App Routes
"""
@app.route("/")
def welcome():
    return config.get("WELCOMING")


@app.route("/search", methods=["GET","POST"])
def get_es_results():
    """GET Method to get the data from Elasticsearch

    Returns:
        [Json]: Ranked Locations
    """

    if request.method == "GET":
        #extract query from request payload
        query = request.args.get("query")
        #extract longitude from request payload
        lon = request.args.get("lon")
        #extract latitude from request payload
        lat = request.args.get("lat")
        # Elasticsearch Query request
        res = es.search(
            index='places',
            body={
                "query": {
                    "match": {
                        "name": {
                            "query": query,
                            "fuzziness": "AUTO"
                        }
                    }
                }
            }
        )
        # create payload
        payload = {"places" : res['hits']['hits'][:5], "query" : query, "lat" : lat, "lon" : lon}
        # send POST request to ml micro-service
        reranked_data = requests.post(url = "https://ml-rerank-service.herokuapp.com/re-rank", json = json.dumps(payload))
        # converit micro-service response to json
        response = jsonify(reranked_data.json())
        #add CORS Header to response
        response.headers.add("Access-Control-Allow-Origin","*")
        return response
    else:
        return config.get("WELCOMING")
"""
Flask App Entry Point (Main)
"""
if __name__ == "__main__":
    #open configuration
    with open("config.json") as json_file:
        # append the json file, to get all of them in on json variable
        config = json.load(json_file)
    # login to elasticsearch
    es = Elasticsearch(
        [config.get("ES_ENDPOINT")],
        http_auth=(config.get("ES_USERNAME"), config.get("ES_PASS")),
    )
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=port)
