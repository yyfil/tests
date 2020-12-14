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


def is_empty():
    pass


def delete_bears():
    pass
