import requests
import time
from parsel import Selector
from tech_news.database import create_news


# Requisito 1
def fetch(url, timeout=3):
    try:
        time.sleep(1)
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
    except (requests.HTTPError, requests.ReadTimeout):
        return None
    else:
        return response.text


# Requisito 2
def scrape_novidades(html_content):
    selector = Selector(html_content)
    return selector.css(
        "div.post-outer div.entry-thumbnail a::attr(href)").getall()


# Requisito 3
def scrape_next_page_link(html_content):
    selector = Selector(html_content)
    return selector.css(
        "div.nav-links a.next.page-numbers::attr(href)").get()


# Requisito 4
def scrape_noticia(html_content):
    selector = Selector(html_content)
    url = selector.css("link[rel='canonical']::attr(href)").get()
    title = selector.css("h1.entry-title::text").get()
    if title is not None:
        title = title.strip()
    timestamp = selector.css("ul.post-meta li.meta-date::text").get()
    if timestamp is not None:
        timestamp = timestamp.split(" ", 1)[0]
    writer = selector.css("span.author a.url.fn.n::text").get()
    comments_count = len(selector.css("ol.comment-list li").getall())
    summary = selector.css(
        "div.entry-content > p:first-of-type ::text").getall()
    summary_ok = "".join(summary).strip()
    tags = selector.css("section.post-tags a::text").getall()
    category = selector.css("a.category-style span.label::text").get()
    dictionary = {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "comments_count": comments_count,
        "summary": summary_ok,
        "tags": tags,
        "category": category
    }
    return dictionary


# Requisito 5
def get_tech_news(amount):
    url = "https://blog.betrybe.com/"
    main_content = fetch(url)
    news_links = scrape_novidades(main_content)
    i = 0
    news = []
    while len(news) < amount:
        news.append(scrape_noticia(fetch(news_links[i])))
        if i == len(news_links) - 1:
            url = scrape_next_page_link(main_content)
            main_content = fetch(url)
            news_links = scrape_novidades(main_content)
            i = 0
        else:
            i += 1
    create_news(news)
    return news
