import json
import logging
from typing import List
from multiprocessing import Process

from extensions import redis_conn
from ortools_utils import run_route_optimizer
import haversine as hs

logging.basicConfig(
    level=logging.INFO,
    format='%(process)d-%(levelname)s-%(message)s'
)
logger = logging.getLogger(__name__)


def process_coordinates(long_lats: List):
    distance_matrix = []
    for lon_lat in long_lats:
        cols = []
        for i in range(len(long_lats)):
            lon_lat_x = lon_lat
            lon_lat_y = long_lats[i]
            distance_ = hs.haversine(lon_lat_x, lon_lat_y, unit=hs.Unit.MILES)
            cols.append(distance_)
        distance_matrix.append(cols)
    data = {"distance_matrix": distance_matrix, "num_vehicles": 1, "depot": 1}
    logger.info(f"ROUTE DATA: {data}\n\n")
    return data


def publish_route_data_to_queue(coordinates: List):
    data = process_coordinates(coordinates)
    try:
        route_data = run_route_optimizer(data)
    except Exception as e:
        logger.info(f"OR-TOOLS Error: {str(e)}\n\n")
        route_data = []
    redis_conn.publish("route-data", json.dumps(route_data))
    optimized_ = " -> ".join(map(str, route_data))
    logger.info(f"OPTIMIZED DATA: {optimized_}\n\n")
    return {"route_data": optimized_}


def get_coordinates_from_queue():
    pub_sub = redis_conn.pubsub()
    pub_sub.subscribe("coordinates")
    for message in pub_sub.listen():
        if message.get("type") == "message":
            coordinates = json.loads(message.get("data"))
            logger.info(f"PUBLISHING: {coordinates}\n\n")
            publish_route_data_to_queue(coordinates)


if __name__ == "__main__":
    Process(target=get_coordinates_from_queue).start()
    logger.info("TRANSMITTING\n\n")
