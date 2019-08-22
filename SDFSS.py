import pandas as pd
import datetime
from dateutil.parser import parse


def sdfss(t_amb, year, month, day, hour, systemType):

    # Furness Efficientcy
    with open("furnaceEff.csv", mode="r") as csv_file:

        furnessEffFile = pd.read_csv(csv_file, delimiter=",")

    if (systemType == "G"):
        furnaseEff = furnessEffFile["Goodman"][0]
    else:
        furnaseEff = furnessEffFile["Bosch"][0]


    # COP
    if (systemType == "G"):

        with open("goodmanCOP.csv", mode="r") as csv_file:

            COParray = pd.read_csv(csv_file, delimiter=",")

    else:
        with open("boschCOP.csv", mode="r") as csv_file:

            COParray = pd.read_csv(csv_file, delimiter=",")

    COP = getCOP(t_amb, COParray)


    #Price of Natual Gas
    with open('fuelPrice.csv', mode='r') as csv_file:

        fuelPrice = pd.read_csv(csv_file, delimiter=',')

    ngPrice = fuelPrice["NG"][month-1] / 10.64 #Convert to per kWh


    #Price of Electricity
    with open('holidays.csv', mode='r') as csv_file:

        holidayList = pd.read_csv(csv_file, delimiter=',', keep_default_na=False)

    with open('tou_period.csv', mode='r') as csv_file:

        touPrice = pd.read_csv(csv_file, delimiter=',')

    i = 0
    holiday = False
    for i in range(9):
        if(holidayList["Month"][i]==month and holidayList["Day"][i]==day):
            holiday = True

    weekNumber = datetime.datetime(year, month, day).weekday()


    if (holiday or weekNumber > 5):
        peakString = "Elec_off_peak"
    else: 
        if hour < 8:
            indHour = 0
        elif hour < 12:
            indHour = 1
        elif hour < 18:
            indHour = 2
        elif hour < 20:
            indHour = 3
        else:
            indHour = 4

        indFinal = (month-1)*5 + indHour

        peakInt = touPrice["tou_period"][indFinal]

        if peakInt == 1:
            peakString = "Elec_off_peak"
        elif peakInt == 2:
            peakString = "Elec_mid_peak"
        else:
            peakString = "Elec_peak"

    elecPrice = fuelPrice[peakString][month - 1]

    elec = COP * ngPrice / (furnaseEff *  elecPrice)

    return [elec,elecPrice, COP, ngPrice, furnaseEff]

def getCOP(mT_amb, mCOParray):
    if(mT_amb >= float(mCOParray.keys()[0])):
        return float(mCOParray[mCOParray.keys()[0]])
    elif(mT_amb <= float(mCOParray.keys()[len(mCOParray.keys())-1])):
        return float(mCOParray[mCOParray.keys()[len(mCOParray.keys())-1]])
    else:
        for i in range(1,len(mCOParray.keys())):
            if(mT_amb >= float(mCOParray.keys()[i]) and mT_amb <= float(mCOParray.keys()[i-1])):
                a = float(mCOParray[mCOParray.keys()[i-1]])
                b = float(mCOParray[mCOParray.keys()[i]])
                c = float(mCOParray.keys()[i-1])
                d = float(mCOParray.keys()[i])

                return a + (mT_amb - c)/(d-c)*(b-a)




