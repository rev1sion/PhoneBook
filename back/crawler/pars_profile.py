import logging
import json
from random import choice
import requests
from multiprocessing import Pool, freeze_support
from bs4 import BeautifulSoup


def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    }
    r = requests.get(url, headers=headers)
    return r.text


def get_links(html):
    soup = BeautifulSoup(html, "lxml")
    doc_list = soup.find('div', class_='doctors__inner')
    links = []
    for doc in doc_list.findAll('div', class_='doc__inner'):
        doc_link = doc.find('span', class_='doc__face').find('a').get('href')
        links.append(doc_link)
        print(links)
        # doc_photo = doc_link.find('img').get('data-aload').split('?')[0]
        # doc_name = doc_link.find('img').get('alt')
        # doc_prof = doc.find('div', class_='doc__prof').text.split('\n')[0]
    return links


def get_doc_info(html, url, phones):
    soup = BeautifulSoup(html, "lxml")
    try:
        doc_surname = soup.find('h1', class_='doc__name').contents[0].strip()
        doc_name = soup.find('h1', class_='doc__name').find('br').next_element.strip()
        doc_full_name = doc_surname + ' ' + doc_name
        print(doc_full_name)
    except Exception as e:
        logging.exception(e)
        print('error')
        doc_name = ''
    try:
        doc_info = soup.find('div', class_='doctor__text').text.strip()
    except Exception as e:
        logging.exception(e)
        print('error')
        doc_info = ''
    try:
        doc_prof = soup.find('div', class_='doc__prof').text.split('   ')[0].strip()
        print(doc_prof)
    except:
        doc_prof = ''
    try:
        doc_photo_link = soup.find('div', class_='doc__photo').find('img').get('src').split('?')[0]
    except:
        doc_photo_link = ''

    data = {
        'url': url,
        'surname': doc_surname,
        'name': doc_name,
        'full_name': doc_full_name,
        'prof': doc_prof,
        'photo': doc_photo_link,
        'phones': phones,
        'info': doc_info,
    }
    return data


def get_random_phone_number():
    nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    mobile = ''
    phone_k = ''
    phone_city = ''
    phone_small = ''

    while len(mobile) != 7:
        mobile += choice(nums)
    while len(phone_k) != 2:
        phone_k += choice(nums)
    while len(phone_city) != 6:
        phone_city += choice(nums)
    while len(phone_small) != 4:
            phone_small += choice(nums)

    phone_mobile = '+380' + '(' + phone_k + ')' + mobile

    phones = {
        'phone_mobile': phone_mobile,
        'phone_city': phone_city,
        'phone_small': phone_small
    }
    print(phones)
    return phones


def write_json(doctors):
    try:
        data = json.load(open('doctors.json', encoding="utf-8"))
    except:
        data = []

    with open('doctors.json', 'w', encoding="utf-8") as f:
        data.append(doctors)
        json.dump(data, f, indent=2, ensure_ascii=False)


"""
    Parse multiprocess
"""


def make_pool(url):
    html = get_html(url)
    data = get_doc_info(html, url, get_random_phone_number())
    write_json(data)


def main():
    url = 'https://chlb.docdoc.ru/doctor'
    all_links = get_links(get_html(url))

    with Pool(3) as process:
        freeze_support()
        print(process)
        process.map(make_pool, all_links)

    # for url in all_links:
    #     print(url)
    #     html = get_html(url)
    #     data = get_doc_info(html, url, get_random_phone_number())
    #     print(data)
    #     write_json(data)
    #  It was optimized


if __name__ == '__main__':
    main()

