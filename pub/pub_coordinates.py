import json
import logging
from random import uniform
from time import sleep
from typing import Generator, Dict, List
from extensions import redis_conn


logging.basicConfig(
    level=logging.INFO,
    format='%(process)d-%(levelname)s-%(message)s'
)
logger = logging.getLogger(__name__)


PAGE = 1
STEP = 10
LENGTH = 10
ITERATE_STOP = 100


def generate_coordinates(**kwargs) -> Generator:
    page, length = kwargs.get('PAGE', 1), kwargs.get('LENGTH', 10)
    return (
        lambda: (uniform(-180, 180), uniform(-90, 90))
        for _ in range(page, length + 1))


def publish_coordinates(data: List) -> Dict:
    try:
        redis_conn.publish("coordinates", json.dumps(data))
    except Exception as e:
        global PAGE
        PAGE = ITERATE_STOP
        logger.error(f"REDIS_ERROR: {str(e)}\n\n", exc_info=True)
        return {"data": None}
    return {"data": data}


def run():
    data_ = [
        tuple(point()) for point in generate_coordinates(PAGE=PAGE, LENGTH=LENGTH)]
    logger.info(f"COORDINATES:: {data_}\n\n")
    publish_coordinates(data_)


if __name__ == "__main__":
    logger.info("CONNECTING\n\n")
    while PAGE < ITERATE_STOP:
        run()
        PAGE = LENGTH
        LENGTH += STEP
        sleep(3)
    redis_conn.close()
    logger.info("DISCONNECTED\n\n")
