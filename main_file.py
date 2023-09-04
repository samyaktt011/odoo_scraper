import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import json


df = pd.read_json("data_patners.json")
final_data = []
for i in json.loads(df.to_json(orient="records"))[0:10]:
    print(i)
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
    response = requests.get(i.get("url"), headers=header)
    soup = BeautifulSoup(response.content,"html.parser")
    temp_main_dict = {}
    contact_details = soup.find("address",class_ = "mb-0")
    temp_main_dict["address_string"] = BeautifulSoup(str(contact_details.find("span",class_ = "w-100 d-block")).replace("<br/>","\n"),"html.parser").text
    temp_main_dict["telephone"] = contact_details.find("span",attrs = {"itemprop":"telephone"}).text
    temp_main_dict["website"] = contact_details.find("span",attrs = {"itemprop":"website"}).text
    temp_main_dict["email"] = contact_details.find("span",attrs = {"itemprop":"email"}).text
    refrence_details = soup.find("div", id = "right_column").find_all("div",class_ = "d-flex mt-3")
    main_ref = []
    for refrence in refrence_details:
        temp_dict_ref = {}
        refrence = refrence.find("div", class_ = "flex-grow-1")
        temp_dict_ref["link"] = refrence.find("a")["href"]
        temp_dict_ref["name"] = refrence.find("a").text
        try:
            temp_dict_ref["description"] = refrence.find("div").text
        except:
            temp_dict_ref["description"] =""

        main_ref.append(temp_dict_ref)
    temp_main_dict["refrence_data"] = main_ref
    final_data.append(temp_main_dict)
    time.sleep(5)
    
df = pd.DataFrame(final_data)
df.to_json("Main.json","records")