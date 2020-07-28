import os

from flask import Flask, render_template, request, make_response
from helpers import *

app = Flask(__name__)

# serve file in html table after reading data from dynamo db
@app.route('/', methods=['GET'])
def home():
    client = request.args.get('client',None)
    print("BEFORESPLITCLIENT", client)
    if client:
        client = client.split(",")
    print("CLIENT", client)
    get_data = get_dynamo_db_data(client_name_lst=client)
    # converttodf = callmethod2()
    return render_template("leibniz.html", data=get_data, client_val = client if client else '')


@app.route('/download', methods=['GET'])
def download():
    client = request.args.get('client',None)
    if client:
        client = client.split(",")
    print("CLIENT", client)
    get_data = get_dynamo_db_data(client_name_lst=client)
        
    # Creates DataFrame.  
    df = pd.DataFrame(get_data)
    resp = make_response(df.to_csv(index=False))
    resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
    resp.headers["Content-Type"] = "text/csv"
    return resp

if __name__ == "__main__":
    app.run(debug=True)
