from os import link

import requests
import bs4
from telebot import types
from io import BytesIO
from bs4 import BeautifulSoup


def get_text_messages(bot, cur_user, message):
    chat_id = message.chat.id
    ms_text = message.text

    if ms_text == "Прислать собаку":
        bot.send_photo(chat_id, photo=get_dogURL(), caption="Вот тебе собачка!")

    elif ms_text == "Прислать кошку":
        bot.send_photo(chat_id, photo=get_foxURL(), caption="Вот тебе кошка!")

    elif ms_text == "Прислать новости":
        bot.send_message(chat_id, text=get_anekdot())


    elif ms_text == "Прислать фильм":
        send_film(bot, chat_id)

    elif ms_text == "Угадай кто?":
        get_ManOrNot(bot, chat_id)


def send_film(bot, chat_id):
    film = get_randomFilm()
    info_str = f"<b>{film['Наименование']}</b>\n" \
               f"Год: {film['Год']}\n" \
               f"Страна: {film['Страна']}\n" \
               f"Жанр: {film['Жанр']}\n" \
               f"Продолжительность: {film['Продолжительность']}"
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Трейлер", url=film["Трейлер_url"])
    btn2 = types.InlineKeyboardButton(text="СМОТРЕТЬ онлайн", url=film["фильм_url"])
    markup.add(btn1, btn2)
    bot.send_photo(chat_id, photo=film['Обложка_url'], caption=info_str, parse_mode='HTML', reply_markup=markup)


def get_anekdot():
    news_list = []
    req_anek = requests.get('https://www.rbc.ru/tags/?tag=наука')
    if req_anek.status_code == 200:
        soup = bs4.BeautifulSoup(req_anek.text, "html.parser")
        result_find = soup.select('.search-item__wrap')

        name = ''
        for result in result_find:
            result_name = result.select("body > div.l-window.l-window-overflow-mob > div.g-relative.g-clear > div.l-col-container > div.l-table > div.g-relative > div > div.l-col-main > div > div.l-row.g-overflow.js-search-container > * > div > a > span > span")
            name = result_name[0].getText()

            result_url = result.select(
                "body > div.l-window.l-window-overflow-mob > div.g-relative.g-clear > div.l-col-container > div.l-table > div.g-relative > div > div.l-col-main > div > div.l-row.g-overflow.js-search-container > * > div > a")
            url = result_url[0].attrs["href"]

            news_list.append((name, url))



        count_news = min(10, len(news_list))
        txt = ""
        for i, news in enumerate(news_list):
            txt += f"{news[0]} {news[1]}\n"
            if i == count_news:
                break
        return txt


def get_foxURL():
    contents = requests.get('https://api.thecatapi.com/v1/images/search').json()
    image_url = contents[0]['url']
    return image_url


def get_dogURL():
    url = ""
    req = requests.get('https://random.dog/woof.json')
    if req.status_code == 200:
        r_json = req.json()
        url = r_json['url']
        # url.split("/")[-1]
    return url


def get_ManOrNot(bot, chat_id):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Проверить",
                                      url="https://vc.ru/dev/58543-thispersondoesnotexist-sayt-generator-realistichnyh-lic")
    markup.add(btn1)

    req = requests.get("https://thispersondoesnotexist.com/image", allow_redirects=True)
    if req.status_code == 200:
        img = BytesIO(req.content)
        bot.send_photo(chat_id, photo=img, reply_markup=markup, caption="Этот человек реален?")


def get_randomFilm():
    url = 'https://randomfilm.ru/'
    infoFilm = {}
    req_film = requests.get(url)
    soup = bs4.BeautifulSoup(req_film.text, "html.parser")
    result_find = soup.find('div', align="center", style="width: 100%")
    infoFilm["Наименование"] = result_find.find("h2").getText()
    names = infoFilm["Наименование"].split(" / ")
    infoFilm["Наименование_rus"] = names[0].strip()
    if len(names) > 1:
        infoFilm["Наименование_eng"] = names[1].strip()

    images = []
    for img in result_find.findAll('img'):
        images.append(url + img.get('src'))
    infoFilm["Обложка_url"] = images[0]

    details = result_find.findAll('td')
    infoFilm["Год"] = details[0].contents[1].strip()
    infoFilm["Страна"] = details[1].contents[1].strip()
    infoFilm["Жанр"] = details[2].contents[1].strip()
    infoFilm["Продолжительность"] = details[3].contents[1].strip()
    infoFilm["Режиссёр"] = details[4].contents[1].strip()
    infoFilm["Актёры"] = details[5].contents[1].strip()
    infoFilm["Трейлер_url"] = url + details[6].contents[0]["href"]
    infoFilm["фильм_url"] = url + details[7].contents[0]["href"]


print(get_anekdot())



