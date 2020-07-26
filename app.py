import os

from flask import Flask, render_template, request
from helpers import *

app = Flask(__name__)

# serve file in html table after reading data from dynamo db
@app.route('/', methods=['GET'])
def home():
    client = request.args.get('client',None)
    get_data = get_dynamo_db_data(client_name=client)
    print(get_data)
    # converttodf = callmethod2()
    return render_template("leibanize.html", data=get_data)

if __name__ == "__main__":
    client=None
    get_data = get_dynamo_db_data(client_name=client)
    print(get_data)
    app.run(debug=True)
