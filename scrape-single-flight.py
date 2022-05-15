from time import sleep, strftime
from random import randint
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import smtplib
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup
import os
import datetime

# Change this to your own chromedriver path!
driver = webdriver.Chrome()  # looks in /usr/local/bin


def srape_flights(from_location, to_location, from_date, flexible=False):

   
    URL = 'https://www.kayak.dk/flights/{from_location}-{to_location}/{from_date}/2adults?sort=bestflight_a'.format(
          from_location=from_location, to_location=to_location, from_date=from_date)

    driver.get(URL)
    sleep(10)

    # close pop up
    # Body id changes every time site loads - So we are using full xpath
    try:
        class_popup_close = '//div[@class = "dDYU-close dDYU-mod-variant-default dDYU-mod-size-default"]'
        driver.find_element_by_xpath(class_popup_close).click()
    except:
        pass

    out_time_list = []

    out_stops = []

    out_durations = []

    out_dates = []

    prices = []
    company_names_list = []

    flight_urls = []

    # Loads 16 results more
    try:
        more_results = '//a[@class = "moreButton"]'
        driver.find_element_by_xpath(more_results).click()
        print('sleeping.....')
        sleep(randint(25, 35))
    except:
        pass
    try:
        more_results = '//a[@class = "moreButton"]'
        driver.find_element_by_xpath(more_results).click()
        print('sleeping.....')
        sleep(randint(25, 35))
    except:
        pass
    try:
        more_results = '//a[@class = "moreButton"]'
        driver.find_element_by_xpath(more_results).click()
        print('sleeping.....')
        sleep(randint(25, 35))
    except:
        pass
    try:
        more_results = '//a[@class = "moreButton"]'
        driver.find_element_by_xpath(more_results).click()
        print('sleeping.....')
        sleep(randint(25, 35))
    except:
        pass
    try:
        more_results = '//a[@class = "moreButton"]'
        driver.find_element_by_xpath(more_results).click()
        print('sleeping.....')
        sleep(randint(25, 35))
    except:
        pass
    try:
        more_results = '//a[@class = "moreButton"]'
        driver.find_element_by_xpath(more_results).click()
        print('sleeping.....')
        sleep(randint(25, 35))
    except:
        pass

    flight_rows = driver.find_elements_by_xpath(
        '//div[@class="resultWrapper"]')
    #print(flight_rows)
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
        # print(price.text)
        prices.append(price.text)

        # company names
        company_names = inner_grid.find(
            "span", {"class": "codeshares-airline-names"}).text
        # print(company_names)
        company_names_list.append(company_names)

        # Link til flight
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

      
        first_flight_times = both_schedules[0].find(
        "div", {"class": "top"})
        out_time = first_flight_times.text.replace('\n', '')
        #print('out time: ' + out_time)
        out_time_list.append(out_time)

        out_stop = both_section_stops[0].text.replace('\n', '')
        #print(out_stop)
        out_stops.append(out_stop)

        out_duration = both_durations[0].text.replace('\n', '')
        #print(out_duration)
        out_durations.append(out_duration)

        out_dates.append(from_date)

           
    cols = (['Destination','Out Date', 'Out Duration',
              'Out Stops', 'Out Time', 'Company names', 'Price', 'Url'])

    flights_df = pd.DataFrame({
        'Destination': to_location,
        'Out Date': out_dates,
        'Out Duration': out_durations,
        'Out Stops': out_stops,
        'Out Time': out_time_list,
        'Company names': company_names_list,
        'Price': prices,
        'Url': flight_urls})[cols]

    # so we can know when it was scraped
    flights_df['timestamp'] = strftime("%Y%m%d-%H%M")
    return flights_df


# consider the start date as 2021-february 1 st
start_date = datetime.date(2022, 7, 19)

# consider the end date as 2021-march 1 st
end_date = datetime.date(2022, 8, 15)

# delta time
delta = datetime.timedelta(days=1)

# 63cy = hele cypern
to_location = '63cy'
# iterate over range of dates
while (start_date <= end_date):
    from_date = start_date.strftime("%Y-%m-%d")
    print('srcaping data from', from_date, "to Cypern", end="\n")
    final_df = srape_flights('CPH', to_location, from_date)
    csv_path = os.getcwd() + \
    "/exam-selenium-momondo-tester/exam-data/flight-scrape-cypern/flight-scrape-{to_location}-{from_date}.csv".format(
        to_location=to_location, from_date=from_date)
    final_df.to_csv(csv_path)

    start_date += delta
    
# 63cy = hele cypern
to_location = '63cy'
from_date = '2022-07-17'
# final_df = srape_flights('CPH', to_location, from_date)
# csv_path = os.getcwd() + \
#     "/exam-selenium-momondo-tester/exam-data/flight-scrape-cypern/flight-scrape-{to_location}-{from_date}.csv".format(to_location=to_location, from_date=from_date)
# final_df.to_csv(csv_path)
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
