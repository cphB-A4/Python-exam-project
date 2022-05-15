#import pandas as 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import boto3
import json

from time import sleep

def lambda_handler(event, context):
    options = Options()
    options.binary_location = '/opt/headless-chromium'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--single-process')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")

    driver = webdriver.Chrome('/opt/chromedriver', chrome_options=options)
    
    
    from_location = 'CPH'
    to_location = 'LCA'
    from_date = '2022-07-11'
    to_date = '2022-07-20-flexible-2days'
   
   
    URL = 'https://www.momondo.dk/flights/{from_location}-{to_location}/{from_date}/{to_date}/2adults?sort=bestflight_a'.format(
         from_location=from_location, to_location=to_location, from_date=from_date, to_date=to_date)

  #kayak = 'https://www.kayak.dk/flights/CPH-LCA/2022-07-14/2022-07-25/2adults?sort=bestflight_a'
    driver.get(URL)
    
    print('start sleep')
    sleep(25)
    print('end sleep')
    test = ""
    try:
       class_popup_close = '//div[@class = "dDYU-close dDYU-mod-variant-default dDYU-mod-size-default"]'

       print(driver.find_element_by_xpath(class_popup_close).click())
    except:
       print('error closing pop up')
       pass
       
    flight_rows = driver.find_elements_by_xpath('//div[@class="resultWrapper"]')
    print(flight_rows)
    
    out_time_list = []
    return_time_list = []

    out_stops = []
    return_stops = []

    out_durations = []
    return_durations = []

    out_dates = []
    return_dates = []

    prices = []
    company_names_list = []

    flight_urls = []
    
    final_msg = ""
    
    for WebElement in flight_rows:
        print(WebElement)
        final_msg = final_msg + '\n'
        elementHTML = WebElement.get_attribute('outerHTML')
        elementSoup = BeautifulSoup(elementHTML, 'html.parser')
        inner_grid = elementSoup.find("div", {"class": "inner-grid keel-grid"})

       # price
        temp_price = inner_grid.find(
            "div", {"class": "col-price result-column js-no-dtog"})
        price = temp_price.find(
           "span", {"class": "price-text"})
       #print(price.text)
        formatted_price = int(price.text[1:-5].replace(".", ""))

        prices.append(formatted_price)
        final_msg = final_msg + str(formatted_price) +" kr." + '\n'

    #company names
        company_names = inner_grid.find(
         "span", {"class": "codeshares-airline-names"}).text
    #print(company_names)
        company_names_list.append(company_names)

    #Link til flight
        link_to_flights = inner_grid.find("div", {"class": "col col-best"})
        link_to_flights = link_to_flights.find('a')['href']

        base_url = "https://kayak.dk"
        scrapped_url = base_url + link_to_flights
        flight_url = scrapped_url.replace("amp;", "")
        flight_urls.append(flight_url)
        final_msg = final_msg + "Url: " +  str(flight_url) +"" + '\n'

    # flight departure, stops, time ...
        flights = inner_grid.find(
        "ol", {"class": "flights"})
        both_schedules = flights.findAll("div", {"class": "section times"})
        both_section_stops = flights.findAll("div", {"class": "section stops"})
        both_durations = flights.find_all(
            "div", {"class": "section duration allow-multi-modal-icons"})

        for i in range(2):
            if i == 0:
                #Flying interval (first flight)
                first_flight_times = both_schedules[i].find(
                    "div", {"class": "top"})
                out_time = first_flight_times.text.replace('\n', '')
                print('out time: ' + out_time)
                out_time_list.append(out_time)
                final_msg = final_msg + "Out time: " +  out_time +"" + '\n'
 
                out_stop = both_section_stops[i].text.replace('\n', '')
                print(out_stop)
                out_stops.append(out_stop)
                final_msg = final_msg + "Out stops: " +  out_time +"" + '\n'
   
                out_duration = both_durations[i].text.replace('\n', '')
                print(out_duration)
                out_durations.append(out_duration)
                final_msg = final_msg + "Out duration: " +  out_duration +"" + '\n'
    
                #time hardcoded for now
                out_dates.append('14 juli')
  
            if i == 1:
                #Flying interval (second flight)
                first_flight_times = both_schedules[i].find(
                    "div", {"class": "top"})
                return_time = first_flight_times.text.replace('\n', '')
                print('return time: ' + return_time)
                return_time_list.append(return_time)
                final_msg = final_msg + "return time: " +  return_time +"" + '\n'
    
                return_stop = both_section_stops[i].text.replace('\n', '')
                print(return_stop)
                return_stops.append(return_stop)
                final_msg = final_msg + "return stops: " +  return_stop +"" + '\n'
   
                return_duration = both_durations[i].text.replace('\n', '')
                print(return_duration)
                return_durations.append(return_duration)
                final_msg = final_msg + "return duration: " +  return_duration +"" + '\n'
    
               #time date hardcoded for now
                return_dates.append('25 juli')
                
    #cols = (['Out Date', 'Return Date', 'Out Duration',
   #         'Return Duration', 'Out Stops', 'Return Stops', 'Out Time', 'Return Time', 'Company names', 'Price', 'Url'])
    #flights_df = pd.DataFrame({
    #  'Out Date': out_dates,
    #  'Return Date': return_dates,
    #  'Out Duration': out_durations,
    #  'Return Duration': return_durations,
    #  'Out Stops': out_stops,
    #  'Return Stops': return_stops,
    #  'Out Time': out_time_list,
    #  'Return Time': return_time_list,
    #  'Company names': company_names_list,
    #  'Price': prices,
    #  'Url': flight_urls})[cols]

    #email_df = flights_df[flights_df["Price"] ==
     #                   flights_df["Price"]].nsmallest(5, 'Price')

    #print(email_df)
    
    #my_dictionary = dict(zip(prices, flight_urls, out_stops))
    #s = json.dumps(my_dictionary)
    
    ses = boto3.client('ses')

    body = final_msg

    ses.send_email(
	Source = 'your_email@gmail.com',
	    Destination = {
		    'ToAddresses': [
			    'your_email@gmail.com'
		    ]
	    },
	    Message = {
		    'Subject': {
			    'Data': 'Cypern Flights',
			    'Charset': 'UTF-8'
		    },
		    'Body': {
			    'Text':{
				    'Data': body,
				    'Charset': 'UTF-8'
			    }
		    }
	    }
    )
    
    response = {
        "statusCode": 200,
        "body": "Selenium Headless Chrome Initialized"
    }

    return response
