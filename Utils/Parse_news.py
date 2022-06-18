def BBC_News_scrape(Search_keyword):
    import requests
    import lxml
    from bs4 import BeautifulSoup
    search_url_BBC="https://www.bbc.co.uk/search?q="+Search_keyword+"&page=1"
    html_page = requests.get(search_url_BBC)

    soup = BeautifulSoup(html_page.content, "lxml")

    links = []
    for link in soup.findAll('a'):
        if "news/" in link.get('href'):
            print(link.get('href'))
            # links.append(link.get('href'))
            html_page_news = requests.get(link.get('href'))

            soup_news = BeautifulSoup(html_page_news.content, "lxml")
            articles=soup_news.find_all(attrs={'data-component':'text-block'})
            Title_news=soup_news.find_all(attrs={'id':'main-heading'})
            detailed_news_article=" ".join([article.text for article in articles])
            import dateutil.parser
            links.append({'Desc':detailed_news_article,
                            'Title':Title_news[0].text,
                            'Date':dateutil.parser.parse(soup_news.find(attrs={'data-testid':"timestamp"})['datetime']).strftime("%d %b,%Y")})
    return(links)