import json
from typing import Generator

from pub.pub_coordinates import generate_coordinates, publish_coordinates, LENGTH


def test_generate_coordinates():
    coordinates = generate_coordinates()
    assert isinstance(coordinates, Generator)
    assert len(list(coordinates)) == LENGTH


def test_publish_coordinates(redis_db, mocker):
    list_data = [tuple(point()) for point in generate_coordinates()]
    assert len(list_data) == LENGTH
    mocker.patch("pub.pub_coordinates.redis_conn", redis_db)
    pb = redis_db.pubsub()
    pb.subscribe('coordinates')
    pb.parse_response()  # consume the sub reply
    pub_data = publish_coordinates(list_data)

    assert pub_data
    with pb:
        parsed_data = json.loads(pb.parse_response()[2::][0])
    assert len(parsed_data) == LENGTH
    assert set(pub_data['data']) <= set([tuple(i) for i in parsed_data])
