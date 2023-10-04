from tkinter import *
from tkinter import messagebox, filedialog
import requests
from bs4 import BeautifulSoup
import plyer
import pandas as pd

def datacollected():
    def notification(title, message):
        plyer.notification.notify(
            title=title,
            message=message,
            app_icon='corona.ico',
            timeout=15
        )

    url = "https://www.worldometers.info/coronavirus/"
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    tbody = soup.find('tbody')
    abc = tbody.find_all('tr')
    countrynotification = cntdata.get()
    if(countrynotification == ""):
        countrynotification = "world"

    serial_number, countries, total_cases, new_cases, total_deaths, new_deaths, total_recovered, active_cases = [
    ], [], [], [], [], [], [], []
    serious_critical, total_cases_permn, total_deaths_permn, total_tests, total_tests_permillion, total_pop = [
    ], [], [], [], [], []

    header = ['serial_number', 'countries', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths', 'total_recovered', 'active_cases',
              'serious_critical', 'total_cases_permn', 'total_deaths_permn', 'total_tests', 'total_tests_permillion', 'total_pop']

    for i in abc:
        id = i.find_all('td')
        if(id[1].text.strip().lower() == countrynotification.lower()):
            totalcases1 = id[2].text.strip()
            newcases = id[3].text.strip()
            totaldeaths = id[4].text.strip()
            newdeaths = id[5].text.strip()
            notification("CORONA RECENT UPDATES OF {}".format(countrynotification),
                         "Total Cases : {}\nTotal Deaths : {}\nNew Cases : {}\nNew Deaths : {}".format(totalcases1, totaldeaths, newcases, newdeaths))

        serial_number.append(id[0].text.strip())
        countries.append(id[1].text.strip())
        total_cases.append(id[2].text.strip())
        new_cases.append(id[3].text.strip())
        total_deaths.append(id[4].text.strip())
        new_deaths.append(id[5].text.strip())
        total_recovered.append(id[6].text.strip())
        active_cases.append(id[7].text.strip())
        serious_critical.append(id[8].text.strip())
        total_cases_permn.append(id[9].text.strip())
        total_deaths_permn.append(id[10].text.strip())
        total_tests.append(id[11].text.strip())
        total_tests_permillion.append(id[12].text.strip())
        total_pop.append(id[13].text.strip())

    dataframe = pd.DataFrame(list(zip(serial_number, countries, total_cases, new_cases, total_deaths, new_deaths, total_recovered,
                             active_cases, serious_critical, total_cases_permn, total_deaths_permn, total_tests, total_tests_permillion, total_pop)), columns=header)

    sorts = dataframe.sort_values('total_cases', ascending=False)
    for a in flist:
        if (a == 'html'):
            path2 = '{}/coronadata.html'.format(path)
            sorts.to_html(r'{}'.format(path2))
        if (a == 'json'):
            path2 = '{}/coronadata.json'.format(path)
            sorts.to_json(r'{}'.format(path2))
        if (a == 'csv'):
            path2 = '{}/coronadata.csv'.format(path)
            sorts.to_csv(r'{}'.format(path2))

    if(len(flist) != 0):
        messagebox.showinfo(
            "Notification", "Corona Record is saved in {}".format(path2), parent=coro)

def downloaddata():
    global path
    if(len(flist) != 0):
        path = filedialog.askdirectory()
    else:
        pass
    datacollected()
    flist.clear()
    Inhtml.configure(state='normal')
    Injson.configure(state='normal')
    Inexcel.configure(state='normal')

def inhtmldownload():
    flist.append('html')
    Inhtml.configure(state='disabled')

def injsondownload():
    flist.append('json')
    Injson.configure(state='disabled')

def inexceldownload():
    flist.append('csv')
    Inexcel.configure(state='disabled')

coro = Tk()
coro.title("Corona Virus Information")
coro.geometry('800x500+200+100')
coro.configure(bg="#ff3333")
coro.iconbitmap('corona.ico')
flist = []
path = ''

mainlabel = Label(coro, text="Corona Virus Live Tracker", font=(
    "new roman", 30, "italic bold"), bg="#e60000", width=33, fg="black", bd=5)
mainlabel.place(x=0, y=0)

label1 = Label(coro, text="Country Name", font=(
    "arial", 25, "bold"), foreground="#3366ff")
label1.place(x=15, y=100)

label2 = Label(coro, text="Download File in", font=(
    "arial", 25, "bold"), foreground="#3366ff")
label2.place(x=15, y=210)

cntdata = StringVar()
entry1 = Entry(coro, textvariable=cntdata, font=(
    "arial", 25, "italic bold"), relief=RIDGE, bd=2, width=28)
entry1.place(x=280, y=100)

Inhtml = Button(coro, text="Html", font=(
    "arial", 20, "italic bold"), bg="#ff5050", foreground="#880808", relief=RIDGE, activebackground="#880808", activeforeground="white", bd=5, width=5, command=inhtmldownload)
Inhtml.place(x=300, y=200)

Injson = Button(coro, text="Json", font=(
    "arial", 20, "italic bold"), bg="#ff5050", foreground="#880808", relief=RIDGE, activebackground="#880808", activeforeground="white", bd=5, width=5, command=injsondownload)
Injson.place(x=420, y=200)

Inexcel = Button(coro, text="Excel", font=(
    "arial", 20, "italic bold"), bg="#ff5050", foreground="#880808", relief=RIDGE, activebackground="#880808", activeforeground="white", bd=5, width=5, command=inexceldownload)
Inexcel.place(x=540, y=200)

submit = Button(coro, text="Submit", font=(
    "arial", 20, "italic bold"), bg="#3399ff", foreground="#0000b3", relief=RIDGE, activebackground="#0000b3", activeforeground="#3399ff", bd=5, width=17, command=downloaddata)
submit.place(x=317, y=300)

coro.mainloop()

