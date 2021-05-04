import pytest
from app import db
from app.models.planet import Planet

def test_get_all_planets_with_no_records(client):
    # Act
    response = client.get("/planets")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

@pytest.fixture
def two_saved_planets(app):
    # Arrange
    ocean_Planet = Planet(name="Ocean Planet", description="watr 4evr",size= "500")
    mountain_Planet = Planet(name="Mountain Planet", description="i luv 2 climb rocks", size= "1")

    db.session.add_all([ocean_Planet, mountain_Planet])
    # Alternatively, we could do
    # db.session.add(ocean_Planet)
    # db.session.add(mountain_Planet)
    db.session.commit()

def test_get_one_planet(client, two_saved_planets):
    # Act
    response = client.get("/planets/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "name": "Ocean Planet",
        "description": "watr 4evr",
        "size": "500"
    }

def test_get_one_planet_no_data(client):
    # Act
    response = client.get("/planets/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404

def test_get_all_planets_with_records(client,two_saved_planets):
    # Act
    response = client.get("/planets")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2

def test_post_one_planet(client):
    # Act
    request_body = {
        "name": "Big Planet",
        "description": "so large",
        "size": "5,012,033,200"
    }
    response = client.post("/planets", json=request_body)

    # Assert
    assert response.status_code == 201