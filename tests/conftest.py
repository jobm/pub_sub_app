import pytest
import fakeredis


@pytest.fixture(scope='module')
def redis_db():
    redis_db_ = fakeredis.FakeStrictRedis()
    yield redis_db_
    redis_db_.close()
