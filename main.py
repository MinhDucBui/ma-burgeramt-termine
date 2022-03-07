import requests
from bs4 import BeautifulSoup
from time import sleep
from plyer import notification
from datetime import datetime
from notify_run import Notify
import sys
URL = "https://tempus-termine.com/termine/index.php?anr=36&sna=Tfe8bf85178a7e455d07aae6ed85f85a3&action=open&page=standortauswahl&tasks=3329&kuerzel=BPA&schlangen=2-6-8-9-10-11-12-13-14-15-16-17-18-19"
NOTIFY_URL = "https://notify.run/mMsATYSyCJ1MD3kMvOT3"


def check_appointment(refresh_rate):
    notify = Notify()
    finding_appointment = True
    while finding_appointment:
        response = requests.get(URL, headers={
            'user-agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'})
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find("div", {"class": "column drittel", "id": "linkespalte"})
        menu = table.find("ul", {"id": "nav_menu2"})
        all_appointments = menu.find_all('p')
        all_names = menu.find_all('a', {"class": "infolink"})
        if len(all_names) != 14:
            notification_desktop("Not all locations found!")

        for index in range(len(all_appointments)):
            title = "Termin frei in {}".format(all_names[index].getText())
            try:
                if "Keine Termine verfügbar" != all_appointments[index].getText():
                    notify.send(title)
                    finding_appointment = False
            except:
                notify.send(title)
                finding_appointment = False

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)
        sleep(refresh_rate)


if __name__ == '__main__':
    refresh_rate = int(sys.argv[1])
    check_appointment(refresh_rate)
