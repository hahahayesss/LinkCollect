import click
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


@click.command()
@click.option("--driver", "-d",
              default=r"D:\chromedriver_76.exe",
              help="Chrome WebDriver.exe location")
@click.option("--options", "-o",
              default="",
              help="Search options")
def start(driver, options):
    print("- / Starting driver")
    driver = webdriver.Chrome(driver)

    job_data = pd.read_csv("../jobs.csv")
    links_list = []
    for index, job in enumerate(job_data.values):
        driver.get("https://www.google.com/")
        search_element = driver.find_element_by_name("q")
        search_element.send_keys("site:linkedin.com/in/ AND \"" + job + "\"")
        search_element.send_keys(Keys.RETURN)

        for x in range(2):
            links_and_texts = driver.find_elements_by_class_name("r")
            for link_and_text in links_and_texts:
                link = link_and_text.find_element_by_css_selector("a").get_attribute("href")
                links_list.append(link)
            driver.find_element_by_id("pnnext").click()

        if index > 10:
            break

    print(len(links_list))
    for link in links_list:
        print(link)

    driver.close()


if __name__ == '__main__':
    start()
