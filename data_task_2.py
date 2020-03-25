import json
import requests


def api_response(url):
    resp = requests.get(url)
    return resp.json()


def data_select(json_data):
    shop_list = []

    for item in json_data:
        office = {}

        office['address'] = item['address']
        office['latlon'] = [item['latitude'], item['longitude']]
        office['name'] = item['name']
        office['phones'] = [phone['phone'] for phone in item['phones']]
        office['working_hours'] = []

        try:
            workdays = 'пн-пт {0} до {1}'.format(item['hoursOfOperation']['workdays']['startStr'],
                                                 item['hoursOfOperation']['workdays']['startStr'])
            office['working_hours'].append(workdays)
        except:
            workdays = ''

        try:
            saturday = 'сб {0} до {1}'.format(item['hoursOfOperation']['saturday']['startStr'],
                                                 item['hoursOfOperation']['saturday']['startStr'])
            office['working_hours'].append(saturday)
        except:
            saturday = ''
        try:

            sunday = 'вс {0} до {1}'.format(item['hoursOfOperation']['sunday']['startStr'],
                                                 item['hoursOfOperation']['sunday']['startStr'])
            office['working_hours'].append(sunday)
        except:
            sunday = ''

        shop_list.append(office)

    return shop_list


def write_file(shop_list):
    TAB = '   '

    with open('office.json', mode='w', encoding='utf-8') as f:
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
    # https: //www.tui.ru/api/office/list/?cityId=413&subwayId=&hoursFrom=&hoursTo=&serviceIds=all&toBeOpenOnHolidays=false
    # BASE_URL = 'https://www.tui.ru/offices/'

    api_url = 'https://www.tui.ru/api/office/list/?cityId='

    city_id = 1
    last_city_id = 500

    full_shop_list = []

    while city_id < last_city_id:
        full_url = (api_url + str(city_id))
        full_shop_list.extend(data_select(api_response(full_url)))
        city_id += 1
    write_file(full_shop_list)


if __name__ == "__main__":
    main()

