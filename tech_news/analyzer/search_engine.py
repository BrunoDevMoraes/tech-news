from tech_news.database import search_news
import datetime


# Requisito 6
def search_by_title(title):
    query = {"title": {"$regex": title, "$options": "i"}}
    return [(news["title"], news["url"]) for news in search_news(query)]


# Requisito 7
def search_by_date(date):
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError('Data inválida')
    else:
        year = date.split('-')[0]
        month = date.split('-')[1]
        day = date.split('-')[2]
        new_date = f"{day}/{month}/{year}"
        query = {"timestamp": new_date}
        return [(news["title"], news["url"]) for news in search_news(query)]


# Requisito 8
def search_by_tag(tag):
    query = {"tags": {"$elemMatch": {"$regex": tag, "$options": "i"}}}
    return [(news["title"], news["url"]) for news in search_news(query)]


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
