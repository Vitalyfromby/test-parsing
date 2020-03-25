import json

import requests
from bs4 import BeautifulSoup


def get_html(url):
    resp = requests.get(url)

    return resp.text


def parsing(html):
    soup = BeautifulSoup(html, 'html.parser')

    PHONE_NUMBER = []
    phones = soup.find_all("span", {"class": "phone-num zphone"})

    for phone in phones:
        PHONE_NUMBER.append(phone.get_text())
    items = soup.find_all(attrs={'class': 'city-item'})
    shop_list = []

    for item in items:
        city = item.find('h4').get_text()
        shops = item.find_all("div", {"class": "shop-list-item"})

        for shop in shops:
            address = ''
            latlon = []
            name = ''
            working_hours = []

            street = shop.find(attrs={'class': 'shop-address'}).get_text()
            address += (city + ', ' + street)
            lat = float(shop['data-shop-latitude'])
            latlon.append(lat)
            lon = float(shop['data-shop-longitude'])
            latlon.append(lon)
            name += shop.find(attrs={'class': 'shop-name'}).get_text()
            hours = shop.find(attrs={'class': 'shop-weekends'}).get_text()
            days = shop.find(attrs={'class': 'shop-work-time'}).get_text()
            working_hours.append((days + ' ' + hours))

            shop_dict = {
                "address": address,
                "latlon": latlon,
                "name": name,
                "phones": PHONE_NUMBER,
                "working_hours": working_hours
            }

            shop_list.append(shop_dict)

    return shop_list


def write_file(shop_list):
    TAB = '   '

    with open('shops.json', mode='w', encoding='utf-8') as f:
        f.write('[\n')

        for shop in shop_list:

            f.write(TAB + '{\n')
            f.write(r'{0}"address": {1},'.format(TAB, json.dumps((shop["address"]), ensure_ascii=False)) + '\n')
            f.write(r'{0}"latlon": {1},'.format(TAB, json.dumps((shop["latlon"]), ensure_ascii=False)) + '\n')
            f.write(r'{0}"name": {1},'.format(TAB, json.dumps((shop["name"]), ensure_ascii=False)) + '\n')
            f.write(r'{0}"phones": {1},'.format(TAB, json.dumps((shop["phones"]), ensure_ascii=False)) + '\n')
            f.write(r'{0}"working_hours": {1}'.format(TAB,
                                                      json.dumps((shop["working_hours"]), ensure_ascii=False)) + '\n')
            if shop is shop_list[-1]:
                f.write(TAB + '}\n\n')
            else:
                f.write(TAB + '},\n\n')

        f.write(']\n')


def main():
    url = 'https://www.mebelshara.ru/contacts'
    shop_list = parsing(get_html(url))
    write_file(shop_list)


if __name__ == "__main__":
    main()

