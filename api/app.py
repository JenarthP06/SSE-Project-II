from flask import Flask, jsonify, request, make_response
import os
from dotenv import load_dotenv
from supabase import create_client
from collections import Counter
from flask_restful import Api, Resource
from flask_cors import CORS


load_dotenv()


app = Flask(__name__)
CORS(app)
api = Api(app)


supabase = create_client(
    os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY")
)


class AddFavourite(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        film = data.get('show')
        country = data.get('country')
        if username and film and country:
            data, count = supabase.table(
                'user-profile'
            ).select("id").eq("username", username).execute()
            userid = data[1] if isinstance(
                data, tuple
            ) and len(data) == 2 else []
            userid = userid[0]['id']
            datacheck, count = (
                supabase
                .table('Favourites')
                .select('*')
                .eq("movie", film)
                .eq("userid", userid)
                .eq("country", country)
                .execute()
            )
            print('ASDASDASDASDASD', datacheck)
            datacheck = datacheck[1]
            if datacheck != []:
                error_response = make_response(
                    jsonify({'message': 'favourite already exists'}), 400
                )
                return error_response
            else:
                supabase.table(
                    'Favourites'
                ).insert({"movie": film, "userid": userid,
                          "country": country}).execute()
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
            data, count = supabase.table(
                'user-profile'
            ).select("id").eq("username", username).execute()
            userid = data[1] if isinstance(
                data, tuple
            ) and len(data) == 2 else []
            userid = userid[0]['id']
            supabase.table('Favourites') \
                .delete() \
                .eq("movie", film) \
                .eq("userid", userid) \
                .execute()
            response = make_response(jsonify({'message': 'success'}), 200)
            return response
        else:
            error_response = make_response(jsonify({'message': 'error'}), 400)
            return error_response


class Favourite(Resource):
    def get(self):
        username = request.args.get('username')
        if username is None:
            data = ['data', []]
            response = data
            return response
        elif username:
            data, count = supabase.table(
                'user-profile'
            ).select("id").eq("username", username).execute()
            userid = data[1] if isinstance(
                data, tuple
            ) and len(data) == 2 else []
            if userid == []:
                error_response = make_response(jsonify(
                    {'message': 'user does not exist'}
                ), 400)
                return error_response
            userid = userid[0]['id']
            data, count = supabase.table(
                'Favourites'
            ).select("movie", "country").eq("userid", userid
                                            ).execute()
            print(data)
            response = jsonify(data)
            return response
        else:
            error_response = make_response(jsonify({'message': 'error'}), 400)
            return error_response


class FavouriteExists(Resource):
    def get(self):
        username = request.args.get('username')
        show = request.args.get('show')
        if username and show:
            data, count = supabase.table(
                'user-profile'
            ).select("id").eq("username", username).execute()
            userid = data[1] if isinstance(
                data, tuple
            ) and len(data) == 2 else []
            userid = userid[0]['id']
            exists, count = supabase.table(
                'Favourites'
            ).select('*').eq("movie", show).eq("userid", userid).execute()
            exists = exists[1] if isinstance(
                exists, tuple
            ) and len(exists) == 2 else []
            if exists != []:
                response = make_response(jsonify({'message': 'success'}), 200)
                return response
            else:
                response = make_response(
                    jsonify({'message': 'show is not favourited'}), 204
                )
                return response
        else:
            error_response = make_response(jsonify({'message': 'error'}), 400)
            return error_response


class Top5Favourites(Resource):
    def get(self):
        data, count = supabase.table('Favourites') \
            .select('movie', 'country') \
            .execute()

        data = data[1]

        movies = [entry['movie'] for entry in data]
        countries = [entry['country'] for entry in data]

        movie_counts = Counter(movies)
        top_5_movies = movie_counts.most_common(5)

        response_data = [
            {'movie': movie, 'count': count,
             'country': countries[movies.index(movie)]}
            for movie, count in top_5_movies
        ]

        response = jsonify(response_data)
        return response


api.add_resource(AddFavourite, '/addfavourite')
api.add_resource(DeleteFavourite, '/deletefavourite')
api.add_resource(Favourite, '/displayfavourite')
api.add_resource(FavouriteExists, '/checkfavourite')
api.add_resource(Top5Favourites, '/topfavourite')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
