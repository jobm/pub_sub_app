import json
from time import sleep

import pytest

from pub.pub_coordinates import generate_coordinates
from app import process_coordinates, get_coordinates_from_queue


def test_process_coordinates():
    coordinates = [tuple(point()) for point in generate_coordinates()]
    data = process_coordinates(coordinates)
    assert data['depot']
    assert data['num_vehicles']
    assert data['distance_matrix']


@pytest.mark.slow
def test_get_coordinates_from_queue(redis_db, mocker):
    mocker.patch("app.redis_conn", redis_db)

    optimized_data_mock = [2, 7, 8, 6, 2, 1]
    mocker.patch("app.run_route_optimizer", optimized_data_mock)

    pb = redis_db.pubsub()
    pb.subscribe('route-data')
    pb.parse_response()
    with mocker.patch('app.get_coordinates_from_queue'):
        # mock both listening to the queue and call to or-tools which happen before
        redis_db.publish("route-data", json.dumps([2, 7, 8, 6, 2, 1]))
        sleep(2)
    with pb:
        parsed_data = json.loads(pb.parse_response()[2::][0])

    assert len(parsed_data) == len(optimized_data_mock)
