import time
import click
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


@click.command()
@click.option("--driver", "-d",
              default=r"/usr/bin/chromedriver",
              help="Chrome WebDriver.exe location")
@click.option("--options", "-o",
              default="",
              help="Search options")
def start(driver, options):
    print("- / Starting driver")
    driver = webdriver.Chrome(driver)

    job_data = pd.read_csv("../jobs.csv").values[0:10]
    links_list = []
    for index, job in enumerate(job_data):
        print("- / Searching... (" + job + ")")
        driver.get("https://www.google.com/")
        search_element = driver.find_element_by_name("q")
        search_element.send_keys("site:linkedin.com/in/ AND \"" + job + "\"")
        search_element.send_keys(Keys.RETURN)

        while len(driver.find_elements_by_id("recaptcha")) > 0:
            time.sleep(1)

        while 1 == 1:
            links_and_texts = driver.find_elements_by_class_name("r")
            for link_and_text in links_and_texts:
                link = link_and_text.find_element_by_css_selector("a").get_attribute("href")
                links_list.append(link)
            if len(driver.find_elements_by_id("pnnext")) > 0:
                driver.find_element_by_id("pnnext").click()
            else:
                break

    driver.close()
    collected_links = pd.DataFrame(links_list, columns=["linkedin_link"])
    collected_links.to_csv("../" + str(int(time.time())) + ".csv")


if __name__ == '__main__':
    start()
