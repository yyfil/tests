import pytest
from aiohttp_requests import requests
from alaska.runner import DockerRunner


class Alaska:
    PORT = 8091
    URL = '0.0.0.0'

    def __init__(self):
        self._started = False
        self._runner = DockerRunner()

    async def wait_for_alaska(self) -> bool:
        for line in self._runner.container.logs(stream=True):
            if b"= ALASKA =" in line:
                return True

    async def start(self) -> str:
        container_id = await self._runner.start()
        self._started = await self.wait_for_alaska()
        return container_id

    async def stop(self):
        await self._runner.stop()

    @property
    def started(self):
        return self._started


if __name__ == '__main__':
    import asyncio

    async def alaska_test():
        alaska = Alaska()
        await alaska.start()
        print(f'Alaska started: {alaska.started}')
        await alaska.stop()

    asyncio.run(alaska_test())
