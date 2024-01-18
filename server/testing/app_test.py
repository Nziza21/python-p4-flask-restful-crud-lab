import json

from app import app
from models import db, Plant

class TestPlant:
    '''Flask application in app.py'''

    def test_plant_by_id_get_route(self):
        '''has a resource available at "/plants/<int:id>".'''
        response = app.test_client().get('/plants/1')
        assert response.status_code == 200

    def test_plant_by_id_get_route_returns_one_plant(self):
        '''returns JSON representing one Plant object at "/plants/<int:id>".'''
        response = app.test_client().get('/plants/1')
        data = json.loads(response.data.decode())

        if response.status_code == 404:
            assert "error" in data
        else:
            assert isinstance(data, dict)
            assert "id" in data

    def test_plant_by_id_patch_route_updates_is_in_stock(self):
        '''returns JSON representing updated Plant object with "is_in_stock" = False at "/plants/<int:id>".'''
        with app.app_context():
            plant_1 = Plant.query.get(1)
            plant_1.is_in_stock = True
            db.session.commit()

        response = app.test_client().patch(
            '/plants/1',
            json={
                "is_in_stock": False,
            }
        )
        data = json.loads(response.data.decode())

        assert isinstance(data, dict)
        assert "id" in data
        assert data["is_in_stock"] is False

    def test_plant_by_id_delete_route_deletes_plant(self):
        '''returns JSON representing updated Plant object at "/plants/<int:id>".'''
        with app.app_context():
            lo = Plant(
                name="Live Oak",
                image="https://www.nwf.org/-/media/NEW-WEBSITE/Shared-Folder/Wildlife/Plants-and-Fungi/plant_southern-live-oak_600x300.ashx",
                price=250.00,
                is_in_stock=False,
            )

            db.session.add(lo)
            db.session.commit()

            response = app.test_client().delete(f'/plants/{lo.id}')
            assert response.status_code == 204  # Use 204 for successful deletion
            assert not Plant.query.get(lo.id)
