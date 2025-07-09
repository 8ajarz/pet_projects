#for successfull execution of the script Lkd profile language must be set to English

import pandas as pd
import sys
from regex import findall, escape
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from datetime import datetime
from random import uniform
import credentials

#decreases amount of a text of the output if an error appear
sys.tracebacklimit = 1

driver = webdriver.Chrome()

lkd_url = "https://www.linkedin.com/login/"
csv_db = credentials.csv_db
login = credentials.login
passwd = credentials.passwd

def gt_counter(fp = credentials.cred_path):
    with open (fp, 'r') as f:
        res = f.read().split("\n")[0].split()[2]
    return int(res)

# func to help avoid Lkd bot detection. The offered range here is (4.45, 6.5)
def hide(where = ""):
    sleep(uniform(4.45, 7.5))
    if where:
        return print(where)
                          
#markers for regex. Because, for some reasons, same type of pages Lkd might be shown with different source code
patterns = [
["defaultLocalizedName&quot;:&quot;", "&quot;,&quot;"],
['<span class="text-body-small inline t-black--light break-words">', '</span>'],
['defaultLocalizedName&amp;quot;:&amp;quot;', "&amp;quot;"],
['"defaultLocalizedName":"', '","$type"']
]

#func to retrieve location from specific place in the person`s webpage. The webpage comes as a text (string)
def regex_string(pattern, txt):
    pattern = escape(pattern[0]) + "(.*?)" + escape(pattern[1])
    return findall(pattern, txt)

#function gets an url of a Lkd profile, retrieves it`s html, retrieves target`s location
#goes to traget`s contacts, retrieves data from it. Returns tuple of data.
def retrieve_data(target_url):
    email = "Unknown"
    phone = "Unknown"
    location = ["Unknown"]
    try:
        driver.get(url=target_url + "/")
        hide()
        if driver.current_url == "https://www.linkedin.com/404/":
            print(f"{target_url} wasn't found")
            return (location[0], "got err 404", "got err 404")
        profile_page_content = driver.page_source
        for el in patterns:
            location = regex_string(el, profile_page_content)
            if location:
                break
    except ValueError:
        print("err #1a", ValueError)
    except Exception as ex:
        print("err #1b", ex)
    hide()
    try:
        driver.get(url= target_url+"/overlay/contact-info/")
        content = driver.find_element(By.XPATH, "/html/body").text
        content = content.split("\n")
        hide()
    except Exception as ex:
        print(f"{target_url} contact info block error:", ex)
    try:
        email = content[content.index("Email") + 1]
    except ValueError:
        pass
    except Exception as ex:
        print("email block error:", ex)
    try:
        phone = content[content.index("Phone") + 1]
    except ValueError:
        pass
    except Exception as ex:
        print("phone block error:", ex)
    if not location:
        location = ["WARNING. This profile wasn`t processed properly"]
    return (location[0], email, phone)

#func to edit file to update the line needed ############this function needs to be tested.
def edit_line(file_path, line_number, msg):
    lines = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        lines[line_number] = msg
    with open(file_path, 'w') as file:
        file.writelines(lines)

#internal service func for bigger fst loop func
def write_data(df, i,  data):
    df.at[i, "Location"] = data[0]
    df.at[i, "Email Address"] = data[1]
    df.at[i, "Telephone"] = data[2]
    return 0

#starting from the counter of unprocessed line in a .csv this func loops over the file hiding from Lkd detection and tries to extract data from there.
#It checks if the .csv was prepared properly. If it the first launch - it adds 2 new columns,
# If everything went OK- it saves collected data and confirmates successful completion of work. Else - it sends a predefined signal.
def fst_loop(starter, path = csv_db, cntr = 0):
    watcher = 0
    sign = "YES"
    df = pd.read_csv(path)
    #to avoid futurewarning about incompatibility with float64 - it is being casted to "object" type
    df = df.astype(object)
    if starter >= df.shape[0]:
        raise ValueError("The program has reached the end of the table. Check your .csv file")
    if 'Unnamed: 1' in df.columns:
            raise ValueError("The file isn`t prepared properly. Remove all rows above the one with column names")
    if starter == 0:
        if "Telephone" in df.columns or "Location" in df.columns:
            raise ValueError(f"The starter is 0, hence your .csv file shold be brand-new, no Telephone nor Location columns")
        else:
            df.insert(6, column = "Location", value="unknown")
            df.insert(5, column = "Telephone", value="unknown")
            print("inserted two columns")
    if df.shape[0] -1 >= (starter + 15):
        ender = starter + 15
    else:
        ender = df.shape[0]
    for i in range(starter, ender):
        try:
            data = retrieve_data(df.at[i, "URL"])
        except Exception as ex:
            print("Data retrieving error", ex) 
            driver.close()
            driver.quit()
            sys.exit("The script did not finish correctly. Check if you weren`t blocked and/or contact with the developer")
        if "@" not in data[1]:
            watcher +=1
        else:
            watcher = 0
        write_data(df, i, data)
        if watcher == 4:
            cntr -= 4
            sign = "NO"
            break
        cntr +=1
    if starter + cntr < 0:
        raise ValueError("Smth went wrong from the very beginning. Check if Lkd didn`t block you or contact the developer")
    else:
        starter += cntr
    df.to_csv(csv_db, index=False)
    return sign, starter

#Lkd currently has a limit of profiled looked over daily up to 200-250 and can block the user profile is the limit was abused
#Hence 2nd loop - allows to loop in iterations to avoid significant loses
def scnd_loop():
    for i in range(4):
        starter = gt_counter()
        res = fst_loop(starter)
        edit_line(credentials.cred_path, 0, f"counter = {res[1]}\n")
        if res[0] == "NO":
            return (f"program stopped at {i + 1} iteration. Check if the profile weren`t blocked by Lkd")
    return ("Both iterations ended up successfully")

def main():
    print("==" * 7)
    print(f"program start: {datetime.now()}")
    try:
        driver.get(url=lkd_url)
        login_window = driver.find_element(By.NAME, "session_key")
        login_window.clear()
        login_window.send_keys(login)
        password_window = driver.find_element(By.NAME, "session_password")
        password_window.clear
        password_window.send_keys(passwd)
        password_window.send_keys(Keys.ENTER) #emulates pressing Enter button
    except Exception as ex:
        print(ex)
    
    print(scnd_loop())    

    driver.close()
    driver.quit()

if __name__ == "__main__":
    main()

