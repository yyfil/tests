import docker
import logging

log = logging.getLogger(__name__)
client = docker.from_env()


class DockerRunner:
    REVISION = '1.0'
    IMAGE = f'azshoo/alaska:{REVISION}'

    def __init__(self, docker_image_tag=REVISION):
        self.docker_image_tag = docker_image_tag
        self.container = None
        self._logs = None

    async def start(self) -> str:
        self.container = client.containers.run(
            DockerRunner.IMAGE,
            detach=True,
            auto_remove=True,
            network_mode="host"
        )
        return self.container.id

    async def stop(self):
        if self.container:
            logs = self.container.logs().split(b'\n')
            for line in logs:
                log.warning(line)
            self.container.kill()


if __name__ == '__main__':
    import asyncio

    async def start_and_stop_container():
        runner = DockerRunner()
        container_id = await runner.start()
        print(container_id)
        await asyncio.sleep(10)
        print(runner.container.logs())
        await runner.stop()

    asyncio.run(start_and_stop_container())
