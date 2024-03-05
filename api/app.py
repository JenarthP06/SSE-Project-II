from flask import Flask, render_template, jsonify, request, make_response
import os
from dotenv import load_dotenv
from supabase import create_client
from azure.eventhub import EventHubConsumerClient
from flask_restful import Api, Resource
import json

load_dotenv()

app = Flask(__name__)
api = Api(app)


supabase = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))

class AddFavourite(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        film = data.get('show')

        if username and film:
            # Assuming you have a 'favorites' table in Supabase
            data, count = supabase.table('user-profile').select("id").eq("username", username).execute()

            # Extract the user ID from the response
            userid = data[1] if isinstance(data, tuple) and len(data) == 2 else []
            userid = userid[0]['id']

            datacheck, count = supabase.table('Favourites').select('*').eq("movie", film).eq("userid", userid).execute()
            print('ASDASDASDASDASD', datacheck)
            datacheck = datacheck[1]
            if datacheck != []:
                error_response = make_response(jsonify({'message': 'favourite already exists'}), 400)
                return error_response


            supabase.table('Favourites').insert({"movie": film, "userid": userid}).execute()
            response = make_response(jsonify({'message': 'success'}), 200)
            return response
        else:
            error_response = make_response(jsonify({'message': 'error'}), 400)
            return error_response
        
class DeleteFavourite(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        film = data.get('show')

        if username and film:
            #supabase logic
            data, count = supabase.table('user-profile').select("id").eq("username", username).execute()

            # Extract the user ID from the response
            userid = data[1] if isinstance(data, tuple) and len(data) == 2 else []
            userid = userid[0]['id']
            supabase.table('Favourites').delete().eq("movie", film).eq("userid", userid).execute()

            response = make_response(jsonify({'message': 'success'}), 200)
            return response
        
        else:
            error_response = make_response(jsonify({'message': 'error'}), 400)
            return error_response
        


class Favourite(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')

        if username:
            #supabase to return all favourites for username]
            data, count = supabase.table('user-profile').select("id").eq("username", username).execute()

            # Extract the user ID from the response
            userid = data[1] if isinstance(data, tuple) and len(data) == 2 else []
            userid = userid[0]['id']
            data, count = supabase.table('Favourites').select("movie").eq("userid", userid).execute()
            response= jsonify(data)
            return response
        
        else:
            error_response = make_response(jsonify({'message': 'error'}), 400)
            return error_response


api.add_resource(AddFavourite, '/addfavourite')
api.add_resource(DeleteFavourite, '/deletefavourite')
api.add_resource(Favourite, '/displayfavourite')

if __name__ == '__main__':
    app.run(debug=True)
    