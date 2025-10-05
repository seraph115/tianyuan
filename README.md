# Tianyuan Project

## 分布式爬虫平台（Scrapy + Kafka + Airflow）

本项目为一个可扩展的分布式爬虫平台，集成 **Scrapy 爬虫框架**、**Kafka 4.1.0（KRaft 模式）消息队列**、**Redis 缓存队列** 以及 **Airflow 3.1.0 调度系统**。通过容器化部署（Docker Compose），支持多节点爬取、任务调度与数据流式处理，适用于大规模数据采集场景。

---

### 技术栈

| 模块 | 说明 |
|------|------|
| **Scrapy 2.13.3** | Python 爬虫框架，负责数据采集与解析 |
| **Kafka 4.1.0 (KRaft)** | 分布式消息队列，用于任务分发与结果汇聚 |
| **Redis 7.x** | 缓存与任务队列辅助 |
| **Airflow 3.1.0** | 调度系统，用于爬虫任务编排与重抓策略 |
| **Docker Compose** | 一键部署与容器编排 |

---

### 目录结构

```bash
crawler-platform/
├─ docker-compose.yml                   # Redis + Kafka (KRaft) + Scrapy 节点
├─ docker-compose.airflow.yml           # Airflow 3.1.0（独立部署）
├─ spider/
│  ├─ Dockerfile                        # Scrapy 镜像构建文件
│  ├─ requirements.txt                  # Python 依赖包清单
│  ├─ scrapy.cfg                        # Scrapy 配置入口
│  └─ proj/
│     ├─ settings.py                    # 爬虫全局设置
│     ├─ pipelines.py                   # 数据处理与存储逻辑
│     └─ spiders/
│        └─ example_spider.py           # 示例爬虫
└─ airflow/
   └─ dags/
      └─ seed_and_recrawl.py            # Airflow DAG：种子投递 + 定期重抓
