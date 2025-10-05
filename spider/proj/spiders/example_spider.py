from __future__ import annotations
import json
import typing as t
import scrapy
from scrapy_redis.spiders import RedisSpider

def need_render(url: str, render_flag: bool | None = None) -> bool:
    if render_flag is not None:
        return bool(render_flag)
    return any(k in url for k in ("render=1", "#/", "?js=1"))

class ExampleSpider(RedisSpider):
    name = "example"
    redis_key = "example:start_urls"

    # 支持两种队列元素：
    # 1) 纯 URL 字符串
    # 2) JSON: {"url":"...", "render":true, "meta":{...}, "priority":10}
    def make_request_from_data(self, data: t.Union[str, bytes]) -> scrapy.Request | None:
        if isinstance(data, bytes):
            data = data.decode("utf-8", "ignore")
        url: str = ""
        meta: dict = {}
        priority: int | None = None
        render_flag: bool | None = None

        if data and data.strip().startswith("{"):
            try:
                obj = json.loads(data)
                url = (obj.get("url") or "").strip()
                meta = obj.get("meta") or {}
                render_flag = obj.get("render")
                priority = obj.get("priority")
            except Exception:
                url = str(data).strip()
        else:
            url = str(data).strip()

        if not url:
            return None

        meta = dict(meta or {})
        if need_render(url, render_flag):
            meta["playwright"] = True
            meta["playwright_include_page"] = False

        req = scrapy.Request(url=url, callback=self.parse, meta=meta, dont_filter=False)
        if isinstance(priority, int):
            req.priority = priority
        return req

    def parse(self, response: scrapy.http.Response):
        title = response.css("title::text").get(default="").strip()
        yield {"url": response.url, "title": title}

        # 发现新链接（交给 redis frontier 去重+排队）
        for href in response.css("a::attr(href)").getall():
            u = response.urljoin(href)
            m = {"playwright": need_render(u)}
            yield scrapy.Request(url=u, callback=self.parse, meta=m, dont_filter=False, priority=10)
