from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
app = Flask(__name__)
api = Api(app)


class Users(Resource):
    def get(self):
        data = pd.read_csv('users.csv')  # lis le fichier csv
        data = data.to_dict()  # convertis les dataframes en dictionnaire
        return {'data': data}, 200  # retourne les data en code OK 200

    def post(self):
        parser = reqparse.RequestParser()  # initialise

        parser.add_argument('userId', required=True)  # ajoute les arguments
        parser.add_argument('name', required=True)
        parser.add_argument('city', required=True)

        args = parser.parse_args()  # structure les données

        # éviter l'erreur 401 si l'utilisateur existe déjà
        data = pd.read_csv('users.csv')

        if args['userId'] in list(data['userId']):
            return {
                       'message': f"'{args['userId']}' already exists."
                   }, 401
        else:
            # créer des nouvelles entrées avec des nouvelles valeurs
            new_data = pd.DataFrame({
                'userId': args['userId'],
                'name': args['name'],
                'city': args['city'],
                'locations': [[]]
            })
            # ajoute les nouvelles valeurs
            data = data.append(new_data, ignore_index=True)
            data.to_csv('users.csv', index=False)  # enregistre dans le CSV
            return {'data': data.to_dict()}, 200

        return {'data': data.to_dict()}, 200

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userId', required=True)
        parser.add_argument('location', required=True)
        args = parser.parse_args()

        # lis le CSV
        data = pd.read_csv('users.csv')

        if args['userId'] in list(data['userId']):
            # evalue les champs de la liste
            data['locations'] = data['locations'].apply(
                lambda x: ast.literal_eval(x)
            )
            # fonction pour sélectionner le user
            user_data = data[data['userId'] == args['userId']]

            # fonction pour mettre à jour le user
            user_data['locations'] = user_data['locations'].values[0] \
                .append(args['location'])


            data.to_csv('users.csv', index=False)
            return {'data': data.to_dict()}, 200

        else:
            return {
                       'message': f"'{args['userId']}' user not found."
                   }, 404


    pass
