# Author: Asick Ahamed
# website: www.asickweb.com
import flask
import requests
import json
from flask import jsonify
BASE_URL = 'https://swapi.co/api/starships/?page=2' #swapi json url 
 


def create_app():
    app = flask.Flask(__name__)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        global swapi_dict
        url = BASE_URL
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        data = requests.get(url, headers=headers).json()
        
        swapi_dict = {'starships':[], 'starships_unknown_hyperdrive':[]} 
    

        for result in data['results']:
            
            if result['hyperdrive_rating'] != 'unknown':
                #amend value to starships array
                swapi_dict['starships'].insert(0, {'name':result['name'],'hyperdrive':result['hyperdrive_rating']})
                # sort by hyperdrive rating
                swapi_dict['starships'] =  sorted(swapi_dict['starships'],key=lambda k: k['hyperdrive'], reverse=False)
               
            else:
                #amend unknown hyperdrive to array
                swapi_dict['starships_unknown_hyperdrive'].insert(0, {'name':result['name']})
 
            
        print(json.dumps(swapi_dict, indent=2, sort_keys=False)) 
        return flask.render_template('index.html',data=swapi_dict)

    @app.route('/results', methods=['GET', 'POST'])
    def data():
        index() 

        output = json.dumps(swapi_dict, indent=2, sort_keys=False) 
        # data will display on the browser
        return output

    return app


if __name__ == "__main__":
    app = create_app()
    # serve the application on port 7410
    app.run(debug=True,host='0.0.0.0', port=7410)