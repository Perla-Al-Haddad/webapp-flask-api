import json
from flask import Flask
from flask import jsonify
import pandas as pd

app = Flask(__name__)


def formatResponse(data):
    if len(data) > 0:
        if type(data) == str:
            response = {"status": "success", "data": json.loads(data)}
        elif (type(data) == list):
            response = {"status": "success", "data": data}
    else:
        response = {"status": "failure", "message": "No data retrived"}
    return jsonify(response)


def getExcel2JSONData(sheet_name):
    xls = pd.read_excel(
        r"resources/climate_change_download_0.xls", sheet_name=sheet_name)
    json_str = xls.to_json(orient='records')
    json_obj = json.loads(json_str)
    return json_obj


recorded_years = [
    "1990",
    "1991",
    "1992",
    "1993",
    "1994",
    "1995",
    "1996",
    "1997",
    "1998",
    "1999",
    "2000",
    "2001",
    "2002",
    "2003",
    "2004",
    "2005",
    "2006",
    "2007",
    "2008",
    "2009",
    "2010",
    "2011"
]


@app.route('/', methods=['GET'])
def hello():
    return 'API Documentation'


@app.route('/GetAllCountries', methods=['GET'])
def get_all_countries():
    json_obj = getExcel2JSONData("Country")
    return formatResponse(json_obj)


@app.route('/GetCountry/<string:ISOCode>', methods=['GET'])
def get_country(ISOCode):
    json_obj = getExcel2JSONData("Country")
    country_row = [x for x in json_obj if x['Country code'] == ISOCode]
    return formatResponse(country_row)


@app.route('/GetCountryCO2Emissions/Total', methods=['GET'])
def get_countries_CO2_emissions_total():
    json_obj = getExcel2JSONData("Data")
    total_co2 = [x for x in json_obj if x['Series code'] == "EN.ATM.CO2E.KT"]
    response = []
    for i in range(len(total_co2)):
        for year in recorded_years:
            item = {}
            item["Year"] = year
            item["Total_CO2_Emissions"] = None if (
                total_co2[i][year] == "..") else total_co2[i][year]
            item["ISO_Code"] = total_co2[i]["Country code"]
            item["Country_Name"] = total_co2[i]["Country name"]
            response.append(item)
    return formatResponse(response)


@app.route('/GetCountryCO2Emissions/Total/<string:ISOCode>', methods=['GET'])
def get_country_CO2_emissions_total(ISOCode):
    json_obj = getExcel2JSONData("Data")
    total_co2 = [x for x in json_obj if (
        x['Series code'] == "EN.ATM.CO2E.KT" and x["Country code"] == ISOCode)]
    response = []
    for i in range(len(total_co2)):
        for year in recorded_years:
            item = {}
            item["Year"] = year
            item["Total_CO2_Emissions"] = None if (
                total_co2[i][year] == "..") else total_co2[i][year]
            item["ISO_Code"] = total_co2[i]["Country code"]
            item["Country_Name"] = total_co2[i]["Country name"]
            response.append(item)
    return formatResponse(response)
