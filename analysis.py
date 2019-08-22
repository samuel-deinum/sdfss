import pandas as pd
from pandas import DataFrame
import datetime
from dateutil.parser import parse

from SDFSS import sdfss




dataFiles = ["nov","dec","jan","feb","mar"]        

sTypes = ["G","B"]                   
modes = ["S","E","NG"]               
tcosts = []
ttemps = []
tswitches = []

for x in range(0,len(dataFiles)):
    with open(dataFiles[x]+"Data.csv", mode='r') as csv_file:
        print(dataFiles[x]+"Data.csv")
        dFile = pd.read_csv(csv_file, delimiter=',' , keep_default_na=False) 

    for y in range(0,len(sTypes)):
        sType = sTypes[y]

        for z in range(0,len(modes)):
            mode = modes[z]


            runName = dataFiles[x] + sTypes[y] + modes[z]

            dates = []
            temps = []
            elecs = []
            switches = []
            demands = []
            costs = []
            elecPrices = []
            COPs = [] 
            ngPrices = []
            furnaseEffs = []

            totalCost = 0
            totalTemp = 0
            totalSwitch = 0
            i = 0
            while dFile["Temp (Â°C)"][i] != "":
                mDate = datetime.datetime.strptime(dFile["ï»¿Date/Time"][i], "%d/%m/%Y %H:%M")
                temp = float(dFile["Temp (Â°C)"][i])

                [elec,elecPrice, COP, ngPrice, furnaseEff] = sdfss(temp, int(mDate.year), int(mDate.month), int(mDate.day), int(mDate.hour), sType)


                demand = -0.1582*temp + 3.3586  

                if mode == "S":
                    if elec>=1:
                        switch = "E"
                        cost = demand*elecPrice/COP
                    else:
                        switch = "NG"
                        cost = demand*ngPrice/furnaseEff

                    if i>0:
                        if switches[i-1] != switch:
                            totalSwitch = totalSwitch + 1

                elif mode == "E":
                    switch = "E"
                    cost = demand*elecPrice/COP
                elif mode == "NG":
                    switch = "NG"
                    cost = demand*ngPrice/furnaseEff 
                else:
                    print("Enter Proper Mode")
                    exit()

                totalCost = totalCost + cost
                totalTemp = totalTemp + temp

                dates.append(mDate)
                temps.append(temp)
                elecs.append(elec)
                switches.append(switch)
                demands.append(demand)
                costs.append(cost)
                elecPrices.append(elecPrice)
                COPs.append(COP)
                ngPrices.append(ngPrice)
                furnaseEffs.append(furnaseEff)

                i = i+1


            test = {
                "Date": dates,
                "Temp": temps,
                "elec": elecs,
                "System": switches,
                "Demand": demands,
                "Cost" : costs,
                "Elec Price": elecPrices,
                "COP": COPs, 
                "NG Price": ngPrices,
                "Efficientcy": furnaseEffs
            }

            df = DataFrame(test, columns= ["Date", "Temp","elec","System", "Demand","Cost", "Elec Price", "COP", "NG Price", "Efficientcy"])

            export_csv = df.to_csv (r"C:\Users\sam\Documents\8th Semester\Capestone\SDFSS\data" + r"\ " + runName +".csv", index = None, header=True)
            
            tcosts.append(totalCost)
            ttemps.append(totalTemp/i)
            tswitches.append(totalSwitch/i)
            print("All DONE!: " + runName)



cost = {
    "Cost": tcosts,
    "Avg Temp": ttemps,
    "Avg Switch": tswitches
}

dfC = DataFrame(cost, columns= ["Cost", "Avg Temp", "Avg Switch"])

export_csv = dfC.to_csv (r"C:\Users\sam\Documents\8th Semester\Capestone\SDFSS\data\METADATA.csv", index = None, header=True)

print("All DONE!: METADATA")
