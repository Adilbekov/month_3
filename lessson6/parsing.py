from bs4 import BeautifulSoup
import requests

def parsing_acipress():
    url = 'https://akipress.org/'
    respons = requests.get(url=url)
    print(respons)
    soup = BeautifulSoup(respons.text, 'lxml')
    # print(soup)
    all_news = soup.find_all('a', class_="newslink")
    # print(all_news)
    n = 0
    for news in all_news:
        n+=1
        print(f'{n}{news.text}')

    with open('news', 'a+', encoding='UTF_8') as news_acipress:
        news_acipress.write(f'{n}) {news_acipress}\n')

# parsing_acipress()


def parsing_sulpak():
    n = 0
    for page in range(1, 7):
        url = f'https://www.sulpak.kg/f/noutbuki?page={page}'
        response = requests.get(url=url)
        soup = BeautifulSoup(response.text, 'lxml')
        all_laptops = soup.find_all('div', class_='product__item-name')
        all_prices = soup.find_all('div', class_='product__item-price')
    
        for laptop, price in zip(all_laptops, all_prices):
            n += 1
            print(n, laptop.text, "".join(price.text.split()))
parsing_sulpak()