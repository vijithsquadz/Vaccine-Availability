import datetime
import json
import requests
from flask import Flask, render_template, request
from requests import Response

app = Flask(__name__)

district_list = {
    "Alappuzha": "301",
    "Ernakulam": "307",
    "Idukki": "306",
    "Kannur": "297",
    "Kasaragod": "295",
    "Kollam": "298",
    "Kottayam": "304",
    "Kozhikode": "305",
    "Malappuram": "302",
    "Palakkad": "308",
    "Pathanamthitta": "300",
    "Thiruvananthapuram": "296",
    "Thrissur": "303",
    "Wayanad": "299"
}


def get_vaccine_price(vaccines, vaccine_name):
    for vaccine in vaccines:
        if vaccine['vaccine'] == vaccine_name:
            return vaccine['fee']


def get_district_code(district_name):
    return district_list[district_name]


def get_all_availability(centers):
    result = """
                <style>
                    table {
                    font-family: arial, sans-serif;
                    border-collapse: separate;
                    width: 100%;
                    }

                    th {
                    border: 1px solid #dddddd;
                    text-align: center;
                    padding: 8px;
                    }

                    td {
                    border: 1px solid #dddddd;
                    text-align: left;
                    padding: 8px;
                    }

                    tr:nth-child(even) {
                    background-color: #dddddd;
                    }
                </style>
                <table>
                    <tr>
                        <th>Date</th>
                        <th>Center</th>
                        <th>District</th>
                        <th>Block</th>
                        <th>Pincode</th>                        
                        <th>Vaccine</th>
                        <th>Age</th>
                        <th>Fee Type</th>
                        <th>Price</th>
                        <th>Availability</th>
                        <th>Dose1 Avaialbility</th>
                        <th>Dose2 Avaialbility</th>
                    </tr>
             """
    available = False

    if centers is None:
        return "No Vaccination centers are available for booking."

    for center in centers:

        for session in center['sessions']:

            if session['available_capacity'] > 0:
                price = get_vaccine_price(center['vaccine_fees'], session['vaccine']) \
                    if 'vaccine_fees' in center.keys() else 0
                res = """
                                <tr>
                                <td nowrap> {date}</td>
                                <td> {center}</td>
                                <td> {district}</td>
                                <td> {block}</td>
                                <td> {pincode}</td>                                  
                                <td> {vaccine}</td>
                                <td> {age_limit}</td>
                                <td> {fee_type}</td>
                                <td> {price}</td>
                                <td> {available_capacity}</td>
                                <td> {available_capacity_dose1}</td>
                                <td> {available_capacity_dose2}</td>
                                </tr>
                              """

                result += res.format(center=center['name'], district=center['district_name'],
                                     block=center['block_name'], pincode=center['pincode'],
                                     date=session['date'],
                                     vaccine=session['vaccine'],
                                     age_limit=str(session['min_age_limit']) + "+",
                                     available_capacity=session['available_capacity'],
                                     available_capacity_dose1=session['available_capacity_dose1'],
                                     available_capacity_dose2=session['available_capacity_dose2'],
                                     fee_type=center['fee_type'],
                                     price=price)

                available = True

    if available:
        return result
    else:
        return "No Vaccination centers are available for booking."


def get_dose1_availability(centers):
    result = """
                <style>
                    table {
                    font-family: arial, sans-serif;
                    border-collapse: separate;
                    width: 100%;
                    }

                    th {
                    border: 1px solid #dddddd;
                    text-align: center;
                    padding: 8px;
                    }

                    td {
                    border: 1px solid #dddddd;
                    text-align: left;
                    padding: 8px;
                    }

                    tr:nth-child(even) {
                    background-color: #dddddd;
                    }
                </style>
                <table>
                    <tr>
                        <th>Date</th>
                        <th>Center</th>
                        <th>District</th>
                        <th>Block</th>
                        <th>Pincode</th>                        
                        <th>Vaccine</th>
                        <th>Age</th>
                        <th>Fee Type</th>
                        <th>Price</th>
                        <th>Dose1 Avaialbility</th>
                    </tr>
             """
    available = False

    if centers is None:
        return "No Vaccination centers are available for booking."

    for center in centers:

        for session in center['sessions']:

            if session['available_capacity_dose1'] > 0:
                price = get_vaccine_price(center['vaccine_fees'], session['vaccine']) \
                    if 'vaccine_fees' in center.keys() else 0
                res = """
                                <tr>
                                <td nowrap> {date}</td>
                                <td> {center}</td>
                                <td> {district}</td>
                                <td> {block}</td>
                                <td> {pincode}</td>                                  
                                <td> {vaccine}</td>
                                <td> {age_limit}</td>
                                <td> {fee_type}</td>
                                <td> {price}</td>
                                <td> {available_capacity_dose1}</td>
                                </tr>
                              """

                result += res.format(center=center['name'], district=center['district_name'],
                                     block=center['block_name'], pincode=center['pincode'],
                                     date=session['date'],
                                     vaccine=session['vaccine'],
                                     age_limit=str(session['min_age_limit']) + "+",
                                     available_capacity_dose1=session['available_capacity_dose1'],
                                     fee_type=center['fee_type'],
                                     price=price)

                available = True

    if available:
        return result
    else:
        return "No Vaccination centers are available for booking."


def get_dose2_availability(centers):
    result = """
                <style>
                    table {
                    font-family: arial, sans-serif;
                    border-collapse: separate;
                    width: 100%;
                    }

                    th {
                    border: 1px solid #dddddd;
                    text-align: center;
                    padding: 8px;
                    }

                    td {
                    border: 1px solid #dddddd;
                    text-align: left;
                    padding: 8px;
                    }

                    tr:nth-child(even) {
                    background-color: #dddddd;
                    }
                </style>
                <table>
                    <tr>
                        <th>Date</th>
                        <th>Center</th>
                        <th>District</th>
                        <th>Block</th>
                        <th>Pincode</th>                        
                        <th>Vaccine</th>
                        <th>Age</th>
                        <th>Fee Type</th>
                        <th>Price</th>
                        <th>Dose2 Avaialbility</th>
                    </tr>
             """
    available = False

    if centers is None:
        return "No Vaccination centers are available for booking."

    for center in centers:

        for session in center['sessions']:

            if session['available_capacity_dose2'] > 0:
                price = get_vaccine_price(center['vaccine_fees'], session['vaccine']) \
                    if 'vaccine_fees' in center.keys() else 0
                res = """
                        <tr>
                        <td nowrap> {date}</td>
                        <td> {center}</td>
                        <td> {district}</td>
                        <td> {block}</td>
                        <td> {pincode}</td>                                  
                        <td> {vaccine}</td>
                        <td> {age_limit}</td>
                        <td> {fee_type}</td>
                        <td> {price}</td>
                        <td> {available_capacity_dose2}</td>
                        </tr>
                      """

                result += res.format(center=center['name'], district=center['district_name'],
                                     block=center['block_name'], pincode=center['pincode'],
                                     date=session['date'],
                                     vaccine=session['vaccine'],
                                     age_limit=str(session['min_age_limit']) + "+",
                                     available_capacity_dose2=session['available_capacity_dose2'],
                                     fee_type=center['fee_type'],
                                     price=price)

                available = True

    if available:
        return result
    else:
        return "No Vaccination centers are available for booking."


def is_vaccine_available(district_name, dose):
    date = datetime.datetime.today().strftime("%d-%m-%Y")

    try:
        url: str = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={" \
                   "id}&date={date} "
        district_code = get_district_code(district_name)
        browser_header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/90.0.4430.93 Safari/537.36",
            "Connection": "keep-alive",
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "hi_IN"
        }
        response: Response = requests.get(url.format(id=district_code, date=date), headers=browser_header)

        if response.ok:
            centers = json.loads(response.text)['centers']
            if dose == "dose1":
                return get_dose1_availability(centers)
            elif dose == "dose2":
                return get_dose2_availability(centers)
            else:
                return get_all_availability(centers)
        else:
            return str(response.status_code)
    except Exception as ex:
        return "Exception occuured !!!. Error: %s" % str(ex)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/get_availability', methods=['POST'])
def vaccine_availability():
    data = request.get_json()
    return is_vaccine_available(data['district'], data['dose'])


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
