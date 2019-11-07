import time
import click
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def _is_exist(driver, element,
              id=False, name=False, class_name=False, css_selector=False, xpath=False):
    elements = []
    if id:
        elements = driver.find_elements_by_id(element)
    elif name:
        elements = driver.find_elements_by_name(element)
    elif class_name:
        elements = driver.find_elements_by_class_name(element)
    elif css_selector:
        elements = driver.find_elements_by_css_selector(element)
    elif xpath:
        elements = driver.find_elements_by_xpath(element)
    return len(elements) > 0


def _next_page(driver):
    if not _is_exist(driver, element="pnnext", id=True):
        return False
    driver.find_element_by_id("pnnext").click()
    return True


def get_job_list(CSV_file, limit):
    raw_list = pd.read_csv(CSV_file).values
    job_list = []
    for data in raw_list:
        if limit == 0:
            break
        if data[2] == 0:
            job_list.append(data)
            limit -= 1
    return raw_list, job_list


def _check_recaptcha(driver):
    return _is_exist(driver, element="recaptcha",
                     id=True)  # or _is_exist(driver, element="rc-anchor-container", id=True)


def search_job(driver, job_text):
    driver.get("https://www.google.com/")
    if not _is_exist(driver, element="q", name=True):
        raise Exception("Search element not found")
    _text_box = driver.find_element_by_name("q")
    _text_box.send_keys("site:linkedin.com/in/ AND \"" + job_text + "\"")
    _text_box.send_keys(Keys.RETURN)


def _collect_links_in_the_page(driver):
    link_list = []
    for link_text in driver.find_elements_by_class_name("r"):
        link_list.append(
            link_text.find_element_by_css_selector("a").get_attribute("href"))
    return link_list


def collect_all(driver):
    full_link_list = []
    while 1 == 1:
        while _check_recaptcha(driver):
            time.sleep(1)
        full_link_list += _collect_links_in_the_page(driver)
        if not _next_page(driver):
            break
    return full_link_list


def _update_list(input_values, value, list_size, file_name):
    mask = input_values[:, 0] == value[0]
    input_values[mask, 2] = int(time.time())
    input_values[mask, 3] = list_size
    input_values[mask, 4] = file_name
    return input_values


def save_links(links, file_name):
    _data = pd.DataFrame(links, columns=["linkedin_link"])
    _data.to_csv(file_name)


def update_csv(csv_file, list):
    _data = pd.DataFrame(list, columns=["job_title",
                                        "time",
                                        "collected",
                                        "file_name"])
    _data.to_csv(csv_file)


@click.command()
@click.option("--driver", "-d",
              default=r"/usr/bin/chromedriver",
              help="Chrome driver location")
@click.option("--csv_file", "-i",
              default=r"/home/mluser/Desktop/LinkCollect/_jobs.csv",
              help="Input CSV file")
@click.option("--search_limit", "-l",
              default=2,
              help="How many searches once")
def start(driver, csv_file, search_limit):
    _driver = webdriver.Chrome(driver)
    full_list, filtered_list = get_job_list(csv_file, search_limit)

    for _data in filtered_list:
        search_job(_driver, _data[1])
        _links = collect_all(_driver)
        save_links(_links, (_data[1] + ".csv"))
        full_list = _update_list(full_list,
                                 _data,
                                 len(_links),
                                 (_data[1] + ".csv"))
        update_csv(csv_file, full_list[:, 1:])

    _driver.close()


if __name__ == '__main__':
    start()
