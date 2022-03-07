import requests
from bs4 import BeautifulSoup
from time import sleep
from plyer import notification
from datetime import datetime


URL = "https://tempus-termine.com/termine/index.php?anr=36&sna=Tfe8bf85178a7e455d07aae6ed85f85a3&action=open&page=standortauswahl&tasks=3329&kuerzel=BPA&schlangen=2-6-8-9-10-11-12-13-14-15-16-17-18-19"


def notification_desktop(title):
    notification.notify(
        title=title,
        message=title,
        app_icon=None,
        timeout=10,
    )


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
                return
        except:
            notification_desktop(title)
            return

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)
        sleep(300)


if __name__ == '__main__':
    check_appointment()
