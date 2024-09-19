import json
import logging

from client import MailClient
from schemas import UserMessageBody
from broker.producer import get_kafka_producer
from settings import Settings


class MailService:
    def __init__(
            self,
            mail_client: MailClient,
    ) -> None:
        self.mail_client: MailClient = mail_client
        self.logger = logging.getLogger(__name__)

    @property
    def settings(self) -> Settings:
        return self.mail_client.settings

    async def consume_mail(self, message: dict) -> None:
        email_body = UserMessageBody(**message)
        correlation_id = email_body.correlation_id
        try:
            await self.send_welcome_email(
                subject=email_body.subject,
                text=email_body.message,
                to=email_body.user_email,
            )
        except Exception as e:
            await self.mail_fail_callback(
                email=email_body.user_email,
                correlation_id=correlation_id,
                exception=str(e),
            )

    async def mail_fail_callback(self, correlation_id, email, exception) -> None:
        self.logger.error(
            f"Failed to send email to {email}. Correlation ID: {correlation_id}. Exception: {exception}"
        )
        callback_email_data = {
            "exception": str(exception),
            "email": email,
            "correlation_id": correlation_id,
        }
        encode_email_data = json.dumps(callback_email_data).encode()
        producer = await get_kafka_producer(settings=self.settings)
        await producer.start()
        try:
            await producer.send(
                topic=self.settings.broker_config.topics.email_callback_topic,
                value=encode_email_data,
            )
        finally:
            await producer.stop()

    async def send_welcome_email(self, subject, text, to) -> None:
        await self.mail_client.send_email_task(subject, text, to)

