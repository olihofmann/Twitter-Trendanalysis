from flask import Flask, request, jsonify, render_template
from time import sleep

from cassandra.cluster import Cluster
from cassandra.query import dict_factory

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.htm")

@app.route("/get_values")
def get_values():
    cluster = Cluster(["cassandra"])
    session = cluster.connect()

    session.set_keyspace('tweet_keyspace')
    session.row_factory = dict_factory

    rows = session.execute("select timestamp, noun, count, retweets, likes from tweets where noun='Adidas'")
    data = []
    for r in rows:
        d = {}
        d["date"] = r["timestamp"].date().strftime('%Y-%m-%d')
        d["value"] = r["count"] + r["retweets"] + r["likes"]
        data.append(d)
    
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
    #app.run(debug=True)