import pytest
from alaska import Alaska


@pytest.fixture
async def unit_under_test():
    uut = Alaska()

    async def _gen():
        await uut.start()
        return uut

    yield _gen

    await uut.stop()


def pytest_configure(config):
    # register an additional marker
    config.addinivalue_line("markers", "testcase_id(id): mark test with test case ID")


def is_empty():
    pass


def delete_bears():
    pass
