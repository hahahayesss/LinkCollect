import click
import pandas as pd

from selenium import webdriver
from linkedin.experience_data import Experience
from linkedin.education_data import Education


def __get_top_card_data(element):
    title = element.find_element_by_css_selector(
        "div > div > div:nth-child(1) > h1").text
    headline = element.find_element_by_css_selector(
        "div > div > div:nth-child(1) > h2").text
    location = element.find_element_by_css_selector(
        "div > div > div:nth-child(1) > h3 > span:nth-child(1)").text
    connection_size = element.find_element_by_css_selector(
        "div > div > div:nth-child(1) > h3 > span.top-card__subline-item.top-card__subline-item--bullet").text

    top_card = {"title": title,
                "headline": headline,
                "location": location,
                "connectionSize": connection_size}
    return top_card


def __get_summary_data(element):
    summary = element.find_element_by_css_selector("p").text
    return summary


def __get_experience_data(element):
    experience_list = Experience(element).get_data()
    print(experience_list)
    # TODO: Parse experience data
    return "None"


def __get_education_data(element):
    education_list = Education(element).get_data()
    print(education_list)
    # TODO: Parse Education data
    return "None"


def __get_volunteering_data(element):
    elements = element.find_elements_by_css_selector("li")
    volunteer_list = []
    for sub_element in elements:
        volunteer_list.append({"title": sub_element.find_element_by_css_selector("div > h3").text,
                               "subTitle": sub_element.find_element_by_css_selector("div > h4").text})
    # print(volunteer_list)
    # TODO: Parse Volunteer data
    return "None"


def __get_certifications_data(element):
    elements = element.find_elements_by_css_selector("li")
    certification_list = []
    for sub_element in elements:
        certification_list.append({"title": sub_element.find_element_by_css_selector("div > h3").text,
                                   "subTitle": sub_element.find_element_by_css_selector("div > h4").text})
    # print(certification_list)
    # TODO: Parse Certification data
    return "None"


def __get_publications_data(element):
    elements = element.find_elements_by_css_selector("li")
    publication_list = []
    for sub_element in elements:
        publication_list.append({"title": sub_element.find_element_by_css_selector("div > h3").text,
                                 "subTitle": sub_element.find_element_by_css_selector("div > h4").text})
    # print(publication_list)
    # TODO: Parse Publication data
    return "None"


def __get_courses_data(element):
    elements = element.find_elements_by_css_selector("li")
    course_list = []
    for sub_element in elements:
        course_list.append({"title": sub_element.find_element_by_css_selector("div > h3").text,
                            "subTitle": sub_element.find_element_by_css_selector("div > h4").text})
    # print(course_list)
    # TODO: Parse Course data
    return "None"


def __get_awards_data(element):
    elements = element.find_elements_by_css_selector("li")
    award_list = []
    for sub_element in elements:
        award_list.append({"title": sub_element.find_element_by_css_selector("div > h3").text,
                           "subTitle": sub_element.find_element_by_css_selector("div > h4").text,
                           "time": sub_element.find_element_by_css_selector("div > div > span > time").text})
    # print(award_list)
    # TODO: Parse Award data
    return "None"


def __get_languages_data(element):
    elements = element.find_elements_by_css_selector("li")
    language_list = []
    for sub_element in elements:
        language_list.append({"title": sub_element.find_element_by_css_selector("div > h3").text,
                              "subTitle": sub_element.find_element_by_css_selector("div > h4").text})
    # print(language_list)
    # TODO: Parse Language data
    return "None"


def __get_organizations_data(element):
    elements = element.find_elements_by_css_selector("li")
    organization_list = []
    for sub_element in elements:
        organization_list.append({"title": sub_element.find_element_by_css_selector("div > h3").text,
                                  "subTitle": sub_element.find_element_by_css_selector("div > h4").text})
    # print(organization_list)
    # TODO: Parse Organization data
    return "None"


def __get_groups_data(element):
    elements = element.find_elements_by_css_selector("li")
    group_list = []
    for sub_element in elements:
        group_list.append(sub_element.find_element_by_css_selector("div > h3").text)
    # print(group_list)
    # TODO: Parse Group data
    return "None"


# ----------------------------------------------------------------------------------------------------------------------

def __exist(driver, css_selector):
    _temp = driver.find_elements_by_css_selector(css_selector)
    if len(_temp) > 0:
        return True
    else:
        return False


# ----------------------------------------------------------------------------------------------------------------------

TOP_CARD = "body > main > section.core-rail > section > section.top-card-layout"
SUMMARY_CARD = "body > main > section.core-rail > section > section.summary.pp-section"
EXPERIENCE_CARD = "body > main > section.core-rail > section > section.experience.pp-section > ul"
EDUCATION_CARD = "body > main > section.core-rail > section > section.education.pp-section > ul"
VOLUNTEER_CARD = "body > main > section.core-rail > section > section.volunteering.pp-section > ul"
CERTIFICATION_CARD = "body > main > section.core-rail > section > section.certifications.pp-section > ul"
PUBLICATION_CAR = "body > main > section.core-rail > section > section.publications.pp-section > ul"
COURSE_CARD = "body > main > section.core-rail > section > section.courses.pp-section > ul"
AWARD_CARD = "body > main > section.core-rail > section > section.awards.pp-section > ul"
LANGUAGE_CARD = "body > main > section.core-rail > section > section.languages.pp-section > ul"
ORGANIZATION_CARD = "body > main > section.core-rail > section > section.organizations.pp-section > ul"
GROUP_CARD = "body > main > section.core-rail > section > section.groups.pp-section > div > ul"


def _get_data(driver, link):
    driver.get(link)
    if driver.title.__contains__("Log In or Sign Up"):
        return None

    full_data = {}
    if __exist(driver, TOP_CARD):
        full_data["topCard"] = __get_top_card_data(
            driver.find_element_by_css_selector(TOP_CARD))
    else:
        full_data["topCard"] = {"title": "", "headline": "", "location": "", "connectionSize": ""}

    if __exist(driver, SUMMARY_CARD):
        full_data["summaryCard"] = __get_summary_data(
            driver.find_element_by_css_selector(SUMMARY_CARD))
    else:
        full_data["summaryCard"] = {}

    if __exist(driver, EXPERIENCE_CARD):
        full_data["experienceCard"] = __get_experience_data(
            driver.find_element_by_css_selector(EXPERIENCE_CARD))
    else:
        full_data["experienceCard"] = {}

    if __exist(driver, EDUCATION_CARD):
        full_data["educationCard"] = __get_education_data(
            driver.find_element_by_css_selector(EDUCATION_CARD))
    else:
        full_data["educationCard"] = {}

    if __exist(driver, VOLUNTEER_CARD):
        full_data["volunteerCard"] = __get_volunteering_data(
            driver.find_element_by_css_selector(VOLUNTEER_CARD))
    else:
        full_data["volunteerCard"] = {}

    if __exist(driver, CERTIFICATION_CARD):
        full_data["certificationCard"] = __get_certifications_data(
            driver.find_element_by_css_selector(CERTIFICATION_CARD))
    else:
        full_data["certificationCard"] = {}

    if __exist(driver, PUBLICATION_CAR):
        full_data["publicationCard"] = __get_publications_data(
            driver.find_element_by_css_selector(PUBLICATION_CAR))
    else:
        full_data["publicationCard"] = {}

    if __exist(driver, COURSE_CARD):
        full_data["courseCard"] = __get_courses_data(
            driver.find_element_by_css_selector(COURSE_CARD))
    else:
        full_data["courseCard"] = {}

    if __exist(driver, AWARD_CARD):
        full_data["awardCard"] = __get_awards_data(
            driver.find_element_by_css_selector(AWARD_CARD))
    else:
        full_data["awardCard"] = {}

    if __exist(driver, LANGUAGE_CARD):
        full_data["languageCard"] = __get_languages_data(
            driver.find_element_by_css_selector(LANGUAGE_CARD))
    else:
        full_data["languageCard"] = {}

    if __exist(driver, ORGANIZATION_CARD):
        full_data["organizationCard"] = __get_organizations_data(
            driver.find_element_by_css_selector(ORGANIZATION_CARD))
    else:
        full_data["organizationCard"] = {}

    if __exist(driver, GROUP_CARD):
        full_data["groupCard"] = __get_groups_data(
            driver.find_element_by_css_selector(GROUP_CARD))
    else:
        full_data["groupCard"] = {}
    return full_data


# @click.option("--", "-",
#               default="",
#               help="")
@click.command()
@click.option("--driver", "-d",
              default=r"D:\chromedriver_76.exe",
              help="Chrome WebDriver.exe location")
@click.option("--input_csv", "-i",
              default="../test.csv",
              help="Linkedin lists")
def start(driver, input_csv):
    print("- / Starting driver")
    driver = webdriver.Chrome(driver)

    print("- / Reading CSV file")
    data = pd.read_csv(input_csv)

    collected_data = []
    for index, link in enumerate(data.values):
        if index > 0:
            driver.close()
            return

        temp_data = _get_data(driver, link[0])
        if temp_data is None:
            driver.close()
            return
        collected_data.append(temp_data)

        if index % 49 == 0:
            print((index + 1), " data collected")

    print("- / Writing the collected data")
    # collected_data.to_csv("collected_data.csv")

    driver.close()
    print("Tada !")


if __name__ == '__main__':
    print()
    print(r"         _ \    _ \   |")
    print(r"   __|  |   |  |   |  __|")
    print(r"  |     |   |  |   |  |")
    print(r" _|    \___/  \___/  \__|")
    print()
    print()
    print("This program writen for BAU - AIS")
    print()
    print()
    # time.sleep(5)

    start()
