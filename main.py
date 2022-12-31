import os
from dotenv import load_dotenv
import datetime
import requests
import json
import csv

def main():
    
    industryAPI_list = ["AGRO", "CONSUMP", "FINCIAL", "INDUS", "PROPCON", "RESOURC", "SERVICE", "TECH"]
    industryAPI_dict = {}
    load_dotenv("SECTOR_API.env")

    #check for api url in dict
    for item in industryAPI_list:
        if item not in industryAPI_dict.keys() or industryAPI_dict[item] != os.getenv(item):
            industryAPI_dict[item] = os.getenv(item)

    #get current date
    now = datetime.datetime.now()
    year = now.year
    month = monthName(now.month)
    day = now.day

    #create folder if not already exist
    folderPath = f"csv/{year}/{month}"
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)

    #create csv file
    filePath = f"csv/{year}/{month}/{day}.csv"

    with open(filePath, "w", newline="") as fp:
        field_names = ["symbol", "sign", "prior", "open", "high", "low", "last", "change", "percentChange", "totalVolume", "marketCap", "industryName", "sectorName"]
        writer = csv.DictWriter(fp, fieldnames=field_names)
        writer.writeheader()

        #loop through list of industry
        for industry in industryAPI_list:
            response = requests.get(industryAPI_dict[industry])
            data_dict = json.loads(response.text)
            subIndices_list = data_dict["composition"]["subIndices"]

            #loop through list of sector
            for sector in subIndices_list:

                #loop through list of stocks
                for stock in sector["stockInfos"]:
                    writer.writerow({"symbol": stock["symbol"], "sign": stock["sign"], "prior": stock["prior"], 
                    "open": stock["open"], "high": stock["high"], "low": stock["low"], "last": stock["last"], 
                    "change": stock["change"], "percentChange": stock["percentChange"], "totalVolume": stock["totalVolume"],
                    "marketCap": stock["marketCap"], "industryName": stock["industryName"], "sectorName": stock["sectorName"]} )

########## END OF main() ##########

def monthName(monthInt):
    return { 1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"}[monthInt]

###################################

if __name__ == "__main__":
    main()