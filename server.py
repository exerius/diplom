from flask import Flask, request
from json import dumps
import analysis
from database_operations import save_to_memory, delete

app = Flask(__name__)

@app.route("/describe")
def describe():
    return dumps(analysis.description(), ensure_ascii=False)


@app.route("/histograms")
def histograms():
    args = request.args
    return dumps(analysis.hist([args.get('column')]))


@app.route("/clustering")
def cluster():
    args = request.args
    return dumps(analysis.clustering(int(args.get('number')), [args.get("column1"), args.get("column2")]))


@app.route("/collection", methods=["POST", "DELETE", "PUT"])
def put_collection():
    if request.method == "POST":
        save_to_memory(request.get_json())
        return "200"
    elif request.method == "DELETE":
        delete(request.get_json()['Наименование'])
        return "200"
