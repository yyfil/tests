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


def pytest_addoption(parser):
    parser.addoption("-T", action="store", metavar="NAME", help="only run tests matching testcase IDs.")


def pytest_configure(config):
    config.addinivalue_line("markers", "testcase_id(id): mark test with test case ID")


def pytest_runtest_setup(item):
    test_id_list = [mark.args[0] for mark in item.iter_markers(name="testcase_id")]
    if test_id_list:
        if item.config.getoption("-T") and item.config.getoption("-T") not in test_id_list:
            pytest.skip("Test is not in set {!r}".format(test_id_list))

