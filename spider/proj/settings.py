import os

BOT_NAME = "proj"
SPIDER_MODULES = ["proj.spiders"]
NEWSPIDER_MODULE = "proj.spiders"

# ---- 分布式 Frontier：scrapy-redis ----
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.PriorityQueue"
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

# ---- 并发/限速 ----
CONCURRENT_REQUESTS = 64
CONCURRENT_REQUESTS_PER_DOMAIN = 8
DOWNLOAD_TIMEOUT = 25
RETRY_ENABLED = True
RETRY_TIMES = 2
AUTOTHROTTLE_ENABLED = True

# ---- Playwright（异步 reactor + 下载器）----
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}
PLAYWRIGHT_BROWSER_TYPE = "chromium"
PLAYWRIGHT_LAUNCH_OPTIONS = {"headless": True}
PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 20000

# ---- Item -> Kafka（示例）----
ITEM_PIPELINES = {
    "proj.pipelines.KafkaItemPipeline": 300,
}

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
KAFKA_TOPIC_ITEMS = os.getenv("KAFKA_TOPIC_ITEMS", "items.out")

LOG_LEVEL = "INFO"
FEED_EXPORT_ENCODING = "utf-8"
