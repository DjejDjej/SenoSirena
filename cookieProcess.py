import json
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from utility import  loadjson,printInLog
from utility import config


#This function converts cookies into json and then into headers format (Needs refine in future, the json converting is actually not needed)
def ProcessCookies(cookies):
    resultcookies = "["
    #this converts to json
    for item in cookies:  
        resultcookies += str(item).replace("'", "\"").replace("True", "true").replace("False", "false") + "," 
    resultcookies = resultcookies[:-1] + "]"

            
    try:      
        cookies_json = json.loads(resultcookies)
        cookiesProcessed = ""
    #Converts cookies to the headers format.
        for item in cookies_json:    
            cookiesProcessed += item["name"]+"="+item["value"]+";"    
        return cookiesProcessed

    except json.JSONDecodeError as e:

        printInLog("error processing cookies","error","GLOBAL")
        return None

    



#Opens up chrome
def get_cookies_after_manual_login(url):           
    # Set up options for the visible Chromium browser
    chrome_options = webdriver.ChromeOptions()
    if(config["chrome_path"] != "auto"):
        chrome_options.binary_location = config["chrome_path"]

    # Set up the webdriver with options
    driver = webdriver.Chrome(options=chrome_options)

    try:
        #Open snow
        driver.get(url)  
        #Wait for user to login      
        WebDriverWait(driver, config["login_wait_time"]).until(EC.url_to_be(url))      
        time.sleep(3)

        cookies = driver.get_cookies()
        
        #Return cookies for login
        return cookies 

    except Exception as e:
        printInLog("error getting cookies","error","GLOBAL")

    
#Add cookies to headers
def addCookiesToHeaders(headers,cookies):
    
    Headers = loadjson(headers)          
    Headers["Cookie"] = ProcessCookies(cookies)             
    return Headers
    