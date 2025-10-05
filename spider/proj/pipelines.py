import json
from confluent_kafka import Producer
from scrapy.utils.project import get_project_settings

class KafkaItemPipeline:
    def __init__(self):
        settings = get_project_settings()
        self.servers = settings.get("KAFKA_BOOTSTRAP_SERVERS")
        self.topic = settings.get("KAFKA_TOPIC_ITEMS")
        self.producer = None

    def open_spider(self, spider):
        conf = {
            "bootstrap.servers": self.servers,
            "enable.idempotence": True,
            "linger.ms": 10,
        }
        self.producer = Producer(conf)

    def process_item(self, item, spider):
        payload = json.dumps(dict(item), ensure_ascii=False).encode("utf-8")
        self.producer.produce(self.topic, payload)
        return item

    def close_spider(self, spider):
        if self.producer:
            self.producer.flush(10)
