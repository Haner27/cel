import logging
from util.kafka import KafkaProducer
from util.datetime import utcnow


class KafkaHandler(logging.Handler):
    """
    往kafaka topic发数据
    """
    def __init__(self, kafka_url, topic):
        super().__init__()
        self.__kafka_url = kafka_url
        self.__topic = topic
        self.__producer = self.get_kafka_producer()

    def get_kafka_producer(self):
        producer = KafkaProducer(self.__kafka_url, self.__topic)
        return producer

    def emit(self, record):
        data = {
            'app_key': record.app_key,
            'ip': record.ip,
            'method': record.method,
            'url': record.url,
            'status_code': record.status_code,
            'created': utcnow().isoformat('T')
        }
        self.__producer.send(data, int(record.created))