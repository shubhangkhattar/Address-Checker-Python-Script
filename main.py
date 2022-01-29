import csv
import requests
import ast
from tqdm import tqdm
import os

url = "https://tools.usps.com/tools/app/ziplookup/zipByAddress"

file_location = "Python Quiz Input - Sheet1.csv"

def processAddress(address):
    session = requests.Session()
    session.headers['User-Agent'] = 'Mozilla/5.0'
    response = session.post(url,address)
    response_dict = ast.literal_eval(response.content.decode('utf-8'))
    return True if response_dict['resultStatus'] == 'SUCCESS' else False

if __name__ == '__main__':

    file_location = os.path.dirname(__file__) + "/" + file_location

    with open(file_location,"r+") as file:
        csv_reader = csv.reader(file)
        csv_writer = csv.writer(file)
        csv_data = list(csv_reader)
        csv_data[0].append('Status')
        address = {}

        for line in tqdm(csv_data[1:]):
            address['companyName'] = line[0]
            address['address1'] = line[1]
            address['city'] = line[2]
            address['state'] = line[3]
            address['zip'] = line[4]
            address['address2'] = ""
            address['urbanCode'] = ""
            status = 'Valid' if processAddress(address) else 'In-Valid'
            line.append(status)

        file.seek(0)
        for line in csv_data:
            csv_writer.writerow(line)

    print("...Done...")