import json
import time

from confluent_kafka import Producer, Consumer, KafkaError
from confluent_kafka.admin import AdminClient, NewTopic

__author__ = 'nengfang.han'


class KafkaProducer(object):
    """
    生产者
    """
    def __init__(self, kafka_url, topic):
        self.__kafka_url = kafka_url
        self.__topic = topic
        self.producer = Producer({
            'bootstrap.servers': self.__kafka_url,
            'log.connection.close': False,
            'request.required.acks': 0,
            'queue.buffering.max.ms': 5000,
            'queue.buffering.max.messages': 10000,
            'batch.num.messages': 200
        })

        self.create_topic()
        self.__partitions = self.producer.list_topics().topics[self.__topic].partitions

    def create_topic(self, num_partitions=3, replication_factor=1):
        if self.__topic not in self.producer.list_topics().topics:
            ac = AdminClient({'bootstrap.servers': self.__kafka_url})
            futmap = ac.create_topics([NewTopic(self.__topic, num_partitions, replication_factor)])
            time.sleep(2)

    def send_log(self, err, msg):
        pass

    def get_target_partition_id(self, key):
        return hash(key) % len(self.__partitions)

    def send(self, data, key):
        target_partition_id = self.get_target_partition_id(key)
        self.producer.produce(self.__topic, json.dumps(data).encode('utf-8'), partition=target_partition_id,
                              callback=self.send_log)

    def flush(self):
        self.producer.flush()


class KafkaConsumer(object):
    """
    消费者
    """
    def __init__(self, kafka_url, topic, group_id):
        self.__kafka_url = kafka_url
        self.__topic = topic
        self.consumer = Consumer({
            'bootstrap.servers': self.__kafka_url,
            'group.id': group_id,
            'default.topic.config': {'auto.offset.reset': 'smallest'}
        })

        assert self.__topic in self.consumer.list_topics().topics, \
            'Kafka.Consumer.init: not found topic[{0}]'.format(self.__topic)

        self.consumer.subscribe([self.__topic])

    def run(self, callbacks=None):
        if callbacks is None:
            callbacks = []

        try:
            while True:
                msg = self.consumer.poll(1)
                if msg is None:
                    continue

                if not msg.error():
                    value = msg.value()
                    try:
                        data = json.loads(value.decode('utf-8'))
                    except Exception as ex:
                        print('[failed][kafka]json.loads message failed: {0}\nvalue: {1}'.format(ex, value))
                    else:
                        print('[succeed][kafka]message received from {0} [{1}] value: {2}'.format(msg.topic(),
                                                                                         msg.partition(),
                                                                                         value))
                        for callback in callbacks:
                            callback(data)

                elif msg.error().code() != KafkaError._PARTITION_EOF:
                    break

        except KeyboardInterrupt as e:
            print('[failed][kafka]KeyboardInterrupt.')

        finally:
            self.consumer.close()


if __name__ == '__main__':
    pass