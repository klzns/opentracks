import os
from service import layer
from otapi import otapi

# import Flask
from flask import *

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    count = otapi.OTAPI_Basic_GetServerCount()
    if count == 0:
        TEMPLATE_FILE = 'addServer.html'
    else:
        TEMPLATE_FILE = 'index.html'
        templateData = { "a": 123 }
        
    return render_template(TEMPLATE_FILE, a = 123)

@app.route('/server', methods=['POST'])
def server():    
    if not request.json or not 'contract' in request.json:
        abort(400)

    contract = str(request.json['contract'])
    result = None
    try:            
        result = otapi.OTAPI_Basic_AddServerContract(str(contract))
    except Exception as error:
        print "Error: ", error
        abort(500)

    if result:
        return 201
    else:
        return jsonify({"error": "Bad contract"}), 400    

if __name__ == '__main__':
    # Open-Transactions setup
    otapi.OTAPI_Basic_AppStartup()
    otapi.OTAPI_Basic_Init()
    otapi.OTAPI_Basic_LoadWallet()

    app.run(use_debugger=True, debug=True,
            use_reloader=False)