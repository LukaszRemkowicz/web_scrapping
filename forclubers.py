import os
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup, SoupStrainer
from fake_useragent import UserAgent

import urllib.request
from forum_account import PASSWORD, USERNAME


BASE_URL = ''

payload = 'dict_form_for_login'

LINK_LIST = []
TOPIC_LIST = []

now = datetime.now()


def eval_simple_function(string):
    first_num = 0
    second_num = 0
    listed = re.findall(r'\+|\*|\-|\%|[0-9]+', string[1:-1])

    multi = False
    div = False
    minus = False
    rest = False
    res_result = False

    for element in listed:
        if element == '*':
            multi = True
        elif element == '/':
            div = True
        elif element == '-':
            minus = True
        elif element == '%':
            rest = True
        elif element == '+':
            first_num += second_num
            second_num = 0
            multi = False
            div = False
            minus = False
            rest = False
        else:
            if multi:
                second_num *= int(element)
                multi = False
            elif div:
                second_num /= int(element)
                div = False
            elif minus:
                second_num -= int(element)
                mins = False
            elif rest:
                second_num %= int(element)
                rest = False
            else:
                second_num += int(element)

    return first_num + second_num


try:
    os.mkdir(datetime.now().strftime('%m.%Y'))
except OSError:
    print('Os Error, couldnt create folder')
    pass

"""Conecting to the serwer and browse trance section"""

with requests.session() as s:
    user_agent = UserAgent()
    header = {'User-Agent': str(user_agent.chrome)}
    s.post(BASE_URL, data=payload, headers=header)
    cookie = s.cookies
    for num_page in range(1, 4):
        trance = s.get(f'website_name/{num_page}', cookies=cookie, headers=header)
        soup = BeautifulSoup(trance.text, parseOnlyThese=SoupStrainer("td"), features="lxml")
        x = soup.findAll("a")
        regex = re.compile(r'trance/[0-9].?')
        empty_lity= []
        for tr in x:
            links = tr.get('href')
            # print(links)
            if links and 'website_name' in links and regex.search(links) and links[-5::].isdigit():
                html_regex = r'(.+)(html)(.+)'
                link = re.sub(html_regex, r'\1\2', links)
                is_there_link = False

                """Check if i downloaded it"""

                with open('check_if_downloaded.txt', 'r') as file:
                    for line in file:
                        if link in line:
                            is_there_link = True

                """If not, add to the download list and to the file"""

                if not is_there_link:
                    TOPIC_LIST.append(link)
                    with open('check_if_downloaded.txt', 'a') as file:
                        file.write(link)
                        file.write('\n')
    print(TOPIC_LIST)

    """Colectting download links"""

    for link in TOPIC_LIST[1::]:
        song = s.get(link, cookies=cookie, headers=header)
        soupe = BeautifulSoup(song.content, parseOnlyThese=SoupStrainer("div"), features="lxml")
        ixor = soupe.findAll('a')
        for trs in ixor:
            links = trs.get('data-url')
            if links and 'zip~~' in links and links not in LINK_LIST:
                LINK_LIST.append(links)

    """colectting download links (in zip~ website) and saving file"""

    for link in LINK_LIST:
        regex = re.compile(r'(.+)(www)(.+)(com)(.+?)(.+)')
        zippy_add = re.sub(regex, r'\1\2\3\4', link)
        zippy_zupa = s.get(link, cookies=cookie, headers=header)
        zippy_lista = []
        soupe = BeautifulSoup(zippy_zupa.text, parseOnlyThese=SoupStrainer("div", id='lrbox'), features="lxml")
        name_zupka = soupe.text
        regex = r'(.+)(Name: )(.+)(Size)(.+)'
        name = re.sub(regex, r'\3', name_zupka.replace('\n', ''))
        zupa_zippy = soupe.findAll('script')
        for zips in zupa_zippy:
            if 'mp3' in str(zips):
                zippy_lista.append(str(zips))
        for i in zippy_lista:
            string_list = i.split(';')
        regex = re.compile(r'(.+)(href = )(.+)')
        su = re.sub(regex, r'\3', str(string_list[0].split('\n')[1]))
        regex = (r'(\")(.+)(\")(.+)(\")(.+)(\")')
        string_one = re.sub(regex, r'\2', su)
        numbers = eval_simple_function(re.sub(regex, r'\4', su)[2:-3].replace(' ', ''))
        string_two = re.sub(regex, r'\6', su)
        link_to_file = zippy_add + string_one + str(numbers) + string_two
        try:
            urllib.request.urlretrieve(link_to_file,
                                       os.path.join(os.getcwd(), datetime.now().strftime('%m.%Y'), name + '.mp3'))
        except OSError:
            pass

stop = datetime.now()
result_time = str(stop - now)
result = re.sub(r'([^\n].*)\.([^\n].*)', r'\1', result_time)
print('result time: ', result, 's')
