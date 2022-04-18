import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException  
from dataclasses import dataclass

# Class that will hold jersey info
@dataclass
class Jerseys:
    title:string
    original_price:float
    sale_price:float
    link:string


# Run Firefox in the background and go westbrook's jerseys in the NBA store
Options = Options()
Options.headless = True
driver = webdriver.Firefox(options=Options)
driver.get("https://www.nbastore.eu/en/russell-westbrook/a-30601660+z-9402503-146906127")


def check_if_more_pages():
    # Check if there are more pages
    return driver.find_elements(by=By.CLASS_NAME, value="next-page")[0].find_elements(by=By.TAG_NAME, value="a")[0].get_attribute('aria-disabled')


def get_jerseys():
    # Extract jersey info
    product_grid = []
    jerseys = []
    product_grid = product_grid + driver.find_elements(by=By.CLASS_NAME, value="column")
    while(not check_if_more_pages()):
        driver.get(driver.find_elements(by=By.CLASS_NAME, value="next-page")[0].find_elements(by=By.TAG_NAME, value="a")[0].get_attribute('href'))
        product_grid = product_grid + driver.find_elements(by=By.CLASS_NAME, value="column")
    for product in product_grid:
        price = product.find_elements(by=By.CLASS_NAME, value="price-card")[0].find_elements(by=By.CLASS_NAME, value="sr-only")
        if len(price) == 2:
            jerseys.append(Jerseys(product.find_elements(by=By.CLASS_NAME, value="product-card-title")[0].find_elements(by=By.TAG_NAME, value="a")[0].text, price[1].text, price[0].text, 
                                product.find_elements(by=By.CLASS_NAME, value="product-card-title")[0].find_elements(by=By.TAG_NAME, value="a")[0].get_attribute('href')))

    #Print results out
    print("-------------------------------------------------------------------------------------------------------------------------------------------------------------")
    for jersey in jerseys:
        print("Title: ", jersey.title)
        print("Sale Price: ", jersey.sale_price)
        print("Original Price: ", jersey.original_price)
        print("Link: ", jersey.link)
        print("-------------------------------------------------------------------------------------------------------------------------------------------------------------")

get_jerseys()
