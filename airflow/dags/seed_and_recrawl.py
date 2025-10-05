from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import os, redis

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

def push_seeds(**_):
    r = redis.from_url(REDIS_URL)
    seeds = [
        "https://example.com",
        "https://example.com/archive?page=1",
        '{"url":"https://news.ycombinator.com","render":true,"priority":1}'
    ]
    for s in seeds:
        r.lpush("example:start_urls", s)

with DAG(
    dag_id="seed_and_recrawl",
    start_date=datetime(2025, 1, 1),
    schedule="0 * * * *",   # Airflow 3.x 用 schedule 字段
    catchup=False,
    tags=["crawler"],
):
    PythonOperator(task_id="push_seeds", python_callable=push_seeds)
