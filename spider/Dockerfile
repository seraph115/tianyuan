FROM mcr.microsoft.com/playwright/python:v1.47.0-jammy

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -U pip && pip install -r requirements.txt

# 安装浏览器（Chromium）
RUN playwright install --with-deps chromium

COPY scrapy.cfg /app/scrapy.cfg
COPY proj /app/proj
COPY scrapyd.conf /etc/scrapyd/scrapyd.conf
WORKDIR /app/proj
ENV PYTHONUNBUFFERED=1
