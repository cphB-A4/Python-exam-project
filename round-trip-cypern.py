from time import sleep, strftime
from random import randint
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import smtplib
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup
import os

#Change this to your own chromedriver path!
driver = webdriver.Chrome()  # looks in /usr/local/bin
def srape_flights(from_location, to_location, from_date, to_date, flexible=False):

  URL = 'https://www.kayak.dk/flights/{from_location}-{to_location}/{from_date}/{to_date}/2adults?sort=bestflight_a'.format(
        from_location=from_location, to_location=to_location, from_date=from_date, to_date=to_date)

  momondo = 'https://www.momondo.dk/flight-search/CPH-63cy/2022-07-14-flexible/2022-07-25-flexible/2adults?sort=bestflight_a'
  #kayak = 'https://www.kayak.dk/flights/CPH-LCA/2022-07-14/2022-07-25/2adults?sort=bestflight_a'
  driver.get(URL)
  sleep(10)

  # close pop up
  # Body id changes every time site loads - So we are using full xpath
  xpath_popup_close = '/html/body/div[45]/div/div[3]/div/div/div[1]'
  # /html/body/div[45]/div/div[3]/div/div/div[1]
  # /html/body/div[14]/div/div[3]/div/div/div[1]
  # /html/body/div[44]/div/div[3]/div/div/div[1]
  # /html/body/div[13]/div/div[3]/div/div/div[1]
  # /html/body/div[15]/div/div[3]/div/div/div[1]
  class_popup_close = '//div[@class = "dDYU-close dDYU-mod-variant-default dDYU-mod-size-default"]'
  driver.find_element_by_xpath(class_popup_close).click()

  # if(len(sel_xpath_popup_close) == 0):
  #    xpath_popup_close = '/html/body/div[14]/div/div[3]/div/div/div[1]'

 

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

  #Loads 16 results more
  try:
        more_results = '//a[@class = "moreButton"]'
        driver.find_element_by_xpath(more_results).click()
        print('sleeping.....')
        sleep(randint(25, 35))
  except:
        pass
  
  flight_rows = driver.find_elements_by_xpath('//div[@class="resultWrapper"]')
  print(flight_rows)
  # convert flights_rows to html so beatufiul soup can understand it
  for WebElement in flight_rows:
    
    elementHTML = WebElement.get_attribute('outerHTML')
    elementSoup = BeautifulSoup(elementHTML, 'html.parser')
    inner_grid = elementSoup.find("div", {"class": "inner-grid keel-grid"})

    # price
    temp_price = inner_grid.find(
        "div", {"class": "col-price result-column js-no-dtog"})
    price = temp_price.find(
        "span", {"class": "price-text"})
    #print(price.text)
    prices.append(price.text)

    #company names
    company_names = inner_grid.find("span", {"class": "codeshares-airline-names"}).text
    #print(company_names)
    company_names_list.append(company_names)

    #Link til flight
    link_to_flights = inner_grid.find("div", {"class": "col col-best"})
    link_to_flights = link_to_flights.find('a')['href']
   
    base_url = "https://kayak.dk"
    scrapped_url = base_url + link_to_flights
    flight_url = scrapped_url.replace("amp;", "")
    flight_urls.append(flight_url)


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

            out_stop = both_section_stops[i].text.replace('\n', '')
            print(out_stop)
            out_stops.append(out_stop)

            out_duration = both_durations[i].text.replace('\n', '')
            print(out_duration)
            out_durations.append(out_duration)

            #time hardcoded for now 
            out_dates.append('14 juli')



        if i == 1:
            #Flying interval (second flight)
            first_flight_times = both_schedules[i].find(
                "div", {"class": "top"})
            return_time = first_flight_times.text.replace('\n', '')
            print('return time: ' + return_time)
            return_time_list.append(return_time)

            return_stop = both_section_stops[i].text.replace('\n', '')
            print(return_stop)
            return_stops.append(return_stop)

            return_duration = both_durations[i].text.replace('\n', '')
            print(return_duration)
            return_durations.append(return_duration)

            #time date hardcoded for now 
            return_dates.append('25 juli')
  cols = (['Out Date', 'Return Date', 'Out Duration',
            'Return Duration', 'Out Stops', 'Return Stops', 'Out Time', 'Return Time', 'Company names', 'Price','Url'])

  flights_df = pd.DataFrame({
    'Out Date': out_dates,
    'Return Date': return_dates,
    'Out Duration': out_durations,
    'Return Duration': return_durations,
    'Out Stops': out_stops,
    'Return Stops': return_stops,
    'Out Time' : out_time_list,
    'Return Time': return_time_list, 
    'Company names': company_names_list,
    'Price': prices,
    'Url': flight_urls})[cols]

    # so we can know when it was scraped
  flights_df['timestamp'] = strftime("%Y%m%d-%H%M")
  return flights_df

#63cy = hele cypern
#118cy = hele italien 
final_df = srape_flights('CPH', 'LCA', '2022-07-14', '2022-07-25')
csv_path = os.getcwd() + "/Python Exam Project/flight-scrape-4-maj.csv"
final_df.to_csv(csv_path)
# class = resultwrapper
# class = inner-grid keel-grid
# for price: class = col-price result-column js-no-dtog
# for price: class = price-text

# Load more results to maximize the scraping
def load_more(driver):
    try:
        more_results = '//a[@class = "moreButton"]'
        driver.find_element_by_xpath(more_results).click()
        print('sleeping.....')
        sleep(randint(25, 35))
    except:
        pass
