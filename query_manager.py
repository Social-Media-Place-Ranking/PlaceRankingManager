"""
Import Necessary Libraries 
"""
from flask import Flask, request, jsonify, json
from elasticsearch import Elasticsearch
import requests
import os

app = Flask(__name__)
es = Elasticsearch(
    ['https://06d4ec43aa3e4460b5239afae619b838.us-central1.gcp.cloud.es.io:9243/'],
    http_auth=("elastic", "d4d2LnnpZ7hjUq74HIjpFYaE"),
)
"""
Flask App Routes
"""
@app.route("/")
def welcome():
    return "Query Manager"

@app.route("/search", methods=["GET"])
def get_es_results():
    """Post Method to get the data from es

    Returns:
        [Json]: Ranked Locations
    """

    if request.method =="GET":
        query = request.args.get("query")
        lon = float(request.args.get("lon"))
        lat = float(request.args.get("lat"))
        res= es.search(
            index='places', 
            body = {
                    "query": {
                        "bool":{
                          "must":{
                                "match":
                                {
                                    "name":
                                    {
                                        "query": query,
                                        "fuzziness": "AUTO",
                                        "operator": "and"
                                    }
                                }
                            },
                        "should": {
                            "distance_feature": {
                            "field": "location",
                            "pivot": "500km",
                            "origin": [lon,lat]
                                }
                            }
                        }
                    }
            }
        ) 
        places = json.dumps(res['hits']['hits'])
        reranked_data = requests.post(url = "https://ml-rerank-service.herokuapp.com/re-rank", json = places)
        return (jsonify(reranked_data.json()))

"""
Flask App Entry Point (Main)
"""
if __name__ == "__main__":
    #load model at app launch
    port = int(os.environ.get('PORT',5000))
    app.run(debug=True, use_reloader=False,host='0.0.0.0', port =port)

