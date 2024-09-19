import json

from aiokafka import AIOKafkaConsumer
from fast_depends import inject, Depends as Dep

from service import MailService
from client import MailClient
from settings import get_settings, Settings


def get_mail_client(settings: Settings) -> MailClient:
    print(10)
    return MailClient(settings=settings)


@inject
async def get_mail_service(settings: Settings = Dep(get_settings)) -> MailService:
    print(11)
    return MailService(
        mail_client=get_mail_client(settings=settings),
    )


def get_kafka_consumer(settings: Settings, topic: str) -> AIOKafkaConsumer:
    return AIOKafkaConsumer(
        topic,
        bootstrap_servers=settings.broker_config.url,
        value_deserializer=lambda message: json.loads(message.decode("utf-8")),
    )


async def consume_message(
        consumer: AIOKafkaConsumer
) -> None:
    mail_service = await get_mail_service()
    await consumer.start()
    try:
        async for message in consumer:
            await mail_service.consume_mail(message.value)
    finally:
        await consumer.stop()

# import json
# from typing import Annotated
#
# import aio_pika
# from aio_pika.abc import AbstractConnection

# async def get_amqp_connection() -> AbstractConnection:
#     settings = get_settings()
#     return await aio_pika.connect_robust(settings.rabbitmq.host)


# async def make_aqm_consumer() -> None:
#     mail_service = get_mail_service()
#     connection = await get_amqp_connection()
#     channel = await connection.channel()
#     queue = await channel.declare_queue(name="email_queue", durable=True)
#     await queue.consume(
#         mail_service.consume_mail,
#     )
