import requests
from bs4 import BeautifulSoup
from time import sleep
from plyer import notification
from datetime import datetime


URL = "https://tempus-termine.com/termine/index.php?anr=36&sna=T944ade0c8194e47704d5d6090171ce65&action=open&page" \
      "=standortauswahl&tasks=3329-3330&kuerzel=BPA-RP&schlangen=2-6-8-9-10-11-12-13-14-15-16-17-18-19 "


def notification_desktop(title):
    notification.notify(
        title=title,
        message=title,
        app_icon=None,
        timeout=10,
    )


def telegram_bot_sendtext(bot_message):
    bot_token = ''  # Enter bot token
    bot_chatID = ''  # Enter bot chatID
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)
    return response.json()


def check_appointment():
    response = requests.get(URL, headers={
        'user-agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'})
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find("div", {"class": "column drittel", "id": "linkespalte"})
    menu = table.find("ul", {"id": "nav_menu2"})
    all_appointments = menu.find_all('p')
    all_names = menu.find_all('a', {"class": "infolink"})
    if all_appointments != 14:
        pass
    for index in range(len(all_appointments)):
        title = "Termin frei in {}".format(all_names[index].getText())
        try:
            if "Keine Termine verfügbar" != all_appointments[index].getText():
                notification_desktop(title)
        except:
            notification_desktop(title)

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)
        sleep(300)


if __name__ == '__main__':
    check_appointment()
