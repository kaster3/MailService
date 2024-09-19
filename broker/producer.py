import asyncio

from aiokafka import AIOKafkaProducer

from settings import Settings


async def get_kafka_producer(settings: Settings) -> AIOKafkaProducer:
    return AIOKafkaProducer(
        bootstrap_servers=settings.broker_config.url,
        loop=asyncio.get_running_loop(),
    )
