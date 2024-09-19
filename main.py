import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fast_depends import inject, Depends as Dep

from dependences import consume_message, get_kafka_consumer
from settings import RunConfig, Settings, get_settings


@inject
@asynccontextmanager
async def lifespan(app: FastAPI, settings: Settings = Dep(get_settings)):
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] [%(asctime)s] %(name)s: %(message)s",
    )
    [
        asyncio.create_task(
            consume_message(
                get_kafka_consumer(
                    settings=settings,
                    topic=topic
                )
            )
        )
        for topic in (
            settings.broker_config.topics.logged_in_notification,
            settings.broker_config.topics.verify_email
        )
    ]

    logging.info("Consumers are started")

    yield


main_app = FastAPI(
    lifespan=lifespan
)


if __name__ == "__main__":
    run_config = RunConfig()
    run_config.run_app()
