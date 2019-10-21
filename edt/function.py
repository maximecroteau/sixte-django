import calendar
import requests
import datetime
from bs4 import BeautifulSoup


def scrap(daterequest):
    request = requests.get(
        "https://edtmobiliteng.wigorservices.net//WebPsDyn.aspx?action=posEDTBEECOME&serverid=C&Tel=maxime.croteau&date=" + daterequest + "")
    page = request.content
    soup = BeautifulSoup(page, "lxml")

    lst = []
    lundi = []
    mardi = []
    mercredi = []
    jeudi = []
    vendredi = []

    cours = soup.find_all("div", {"class": "Case"})
    dates = soup.find_all("td", {"class": "TCJour"})

    if cours[0].text == "Pas de cours cette semaine":
        dic = {}
        dic["day"] = "Pas cours cette semaine"
        lst.append(dic)
        lundi.append(dic)
        mardi.append(dic)
        mercredi.append(dic)
        jeudi.append(dic)
        vendredi.append(dic)

    else:
        for c in cours:
            dic = {}
            id_day = c["style"].split(";")[3].split(":")[1].split(".")[0]
            if id_day == "103":
                day = "Lundi"
                date = dates[5].text
            elif id_day == "122":
                day = "Mardi"
                date = dates[6].text
            elif id_day == "141":
                day = "Mercredi"
                date = dates[7].text
            elif id_day == "161":
                day = "Jeudi"
                date = dates[8].text
            elif id_day == "180":
                day = "Vendredi"
                date = dates[9].text
            else:
                day = "none"

            if day != "none":
                hours = c.find("td", {"class": "TChdeb"}).string
                from_hours = hours.split("-")[0].replace(" ", "")
                to_hours = hours.split("-")[1].replace(" ", "")
                name = c.find("td", {"class": "TCase"}).text
                classroom = c.find("td", {"class": "TCSalle"}).text.split(":")[1]
                teacher = c.find("td", {"class": "TCProf"}).text.split("I2")[0].capitalize()
                if teacher == "":
                    teacher = "none"

                dic["day"] = day
                dic["date"] = date
                dic["from_hours"] = from_hours
                dic["to_hours"] = to_hours
                dic["name"] = name
                dic["classroom"] = classroom
                dic["teacher"] = teacher

                tday = find_day(daterequest)
                if day == tday:
                    lst.append(dic)
                if day == "Lundi":
                    lundi.append(dic)
                if day == "Mardi":
                    mardi.append(dic)
                if day == "Mercredi":
                    mercredi.append(dic)
                if day == "Jeudi":
                    jeudi.append(dic)
                if day == "Vendredi":
                    vendredi.append(dic)

    return lst, lundi, mardi, mercredi, jeudi, vendredi


def find_day(date):
    tmp = datetime.datetime.strptime(date, '%m/%d/%Y').weekday()
    name = calendar.day_name[tmp]

    if name == 'Monday':
        day = 'Lundi'
    elif name == 'Tuesday':
        day = 'Mardi'
    elif name == 'Wednesday':
        day = 'Mercredi'
    elif name == 'Thursday':
        day = 'Jeudi'
    elif name == 'Friday':
        day = 'Vendredi'
    elif name == 'Saturday':
        day = 'Samedi'
    elif name == 'Sunday':
        day = 'Dimanche'

    return day
