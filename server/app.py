from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class AllPlants(Resource):
    def get(self):
        all_plants_data = [] 
        return jsonify(all_plants_data)

class SinglePlant(Resource):
    def get(self, id):
        plant_data = {}  
        return jsonify(plant_data)

class UpdatePlant(Resource):
    def patch(self, id):
        data = request.get_json()

        plant = Plant.query.get(id)

        if not plant:
            return make_response(jsonify({'error': 'Plant not found'}), 404)

        if 'is_in_stock' in data:
            plant.is_in_stock = data['is_in_stock']


        db.session.commit()

        return make_response(jsonify(plant.to_dict()), 200)

class DestroyPlant(Resource):
    def delete(self, id):
        plant = Plant.query.get(id)

        if not plant:
            return make_response(jsonify({'error': 'Plant not found'}), 404)

        db.session.delete(plant)
        db.session.commit()

        return make_response('', 204)

api.add_resource(AllPlants, '/plants')
api.add_resource(SinglePlant, '/plants/<int:id>')
api.add_resource(UpdatePlant, '/plants/<int:id>')
api.add_resource(DestroyPlant, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
