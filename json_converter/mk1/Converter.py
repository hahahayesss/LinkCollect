import os
import time
import json
import click
import numpy as np
import pandas as pd

SEPARATOR_0 = "#-[0]-#"
SEPARATOR_1 = "#-[1]-#"


def __list_to_text(_list):
    if len(_list) > 0:
        _full_text = ""
        for _data in _list:
            _full_text += _data + SEPARATOR_0
        return _full_text[:-7]
    else:
        return None


def __date_range(_date_range):
    if _date_range is None:
        return str(None)
    elif len(_date_range.split("–")) > 1:
        _temp = str(_date_range.split("–")[0].strip())
        _temp += SEPARATOR_1
        _temp += str(_date_range.split("–")[1].strip())
        return _temp
    else:
        return str(_date_range.strip())


def __jobs(jobs_info):
    _full_job_text = ""
    for _job in jobs_info:
        _temp = str(_job["title"])
        _temp += SEPARATOR_1
        _temp += str(_job["company"])
        _temp += SEPARATOR_1
        _temp += __date_range(_job["date_range"])
        _temp += SEPARATOR_1
        _temp += str(_job["location"])
        _temp += SEPARATOR_1
        _temp += str(_job["description"])
        _temp += SEPARATOR_1

        if _job["li_company_url"] == "":
            _temp += "0"
        else:
            _temp += "1"
        _full_job_text += _temp + SEPARATOR_0
    return _full_job_text[:-7]


def __education(education_info):
    _full_education_text = ""
    for _education in education_info:
        _temp = str(_education["name"])
        _temp += SEPARATOR_1
        _temp += str(_education["degree"])
        _temp += SEPARATOR_1
        _temp += str(_education["grades"])
        _temp += SEPARATOR_1
        _temp += str(_education["field_of_study"])
        _temp += SEPARATOR_1
        _temp += __date_range(_education["date_range"])
        _temp += SEPARATOR_1
        _temp += str(_education["activities"])
        _full_education_text += _temp + SEPARATOR_0
    return _full_education_text[:-7]


def __volunteering(volunteering_info):
    _full_volunteering_text = ""
    for _volunteering in volunteering_info:
        _temp = str(_volunteering["title"])
        _temp += SEPARATOR_1
        _temp += str(_volunteering["company"])
        _temp += SEPARATOR_1
        _temp += __date_range(_volunteering["date_range"])
        _temp += SEPARATOR_1
        _temp += str(_volunteering["location"])
        _temp += SEPARATOR_1
        _temp += str(_volunteering["cause"])
        _temp += SEPARATOR_1
        _temp += str(_volunteering["description"])
        _full_volunteering_text += _temp + SEPARATOR_0
    return _full_volunteering_text[:-7]


def _personal_info(row, personal_info):
    row.append(personal_info["name"])
    row.append(personal_info["headline"])
    row.append(personal_info["company"])
    row.append(personal_info["school"])
    row.append(personal_info["location"])
    row.append(personal_info["summary"])

    if personal_info["image"] == "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7":
        row.append(None)
    else:
        row.append(personal_info["image"])

    row.append(personal_info["followers"])
    row.append(personal_info["email"])
    row.append(personal_info["phone"])
    row.append(personal_info["connected"])
    row.append(__list_to_text(personal_info["websites"]))
    row.append(personal_info["current_company_link"])
    return row


def _experiences(row, experiences_info):
    if len(experiences_info["jobs"]) > 0:
        row.append(__jobs(experiences_info["jobs"]))
        row.append(len(experiences_info["jobs"]))
    else:
        row.append(None)

    if len(experiences_info["education"]) > 0:
        row.append(__education(experiences_info["education"]))
        row.append(len(experiences_info["education"]))
    else:
        row.append(None)

    if len(experiences_info["volunteering"]) > 0:
        row.append(__volunteering(experiences_info["volunteering"]))
        row.append(len(experiences_info["volunteering"]))
    else:
        row.append(None)
    return row


def _skills(skills_info):
    _full_skills_text = ""
    for _skill in skills_info:
        _temp = str(_skill["name"])
        _temp += SEPARATOR_1
        _temp += str(_skill["endorsements"])
        _full_skills_text += _temp + SEPARATOR_0
    return _full_skills_text[:-7]


def _accomplishments(row, accomplishments_info):
    row.append(__list_to_text(accomplishments_info["publications"]))
    row.append(len(accomplishments_info["publications"]))

    row.append(__list_to_text(accomplishments_info["certifications"]))
    row.append(len(accomplishments_info["certifications"]))

    row.append(__list_to_text(accomplishments_info["patents"]))
    row.append(len(accomplishments_info["patents"]))

    row.append(__list_to_text(accomplishments_info["courses"]))
    row.append(len(accomplishments_info["courses"]))

    row.append(__list_to_text(accomplishments_info["projects"]))
    row.append(len(accomplishments_info["projects"]))

    row.append(__list_to_text(accomplishments_info["honors"]))
    row.append(len(accomplishments_info["honors"]))

    row.append(__list_to_text(accomplishments_info["test_scores"]))
    row.append(len(accomplishments_info["test_scores"]))

    row.append(__list_to_text(accomplishments_info["languages"]))
    row.append(len(accomplishments_info["languages"]))

    row.append(__list_to_text(accomplishments_info["organizations"]))
    row.append(len(accomplishments_info["organizations"]))
    return row


def create_row(row_info):
    _row = []
    _row = _personal_info(_row, row_info["personal_info"])
    _row = _experiences(_row, row_info["experiences"])
    _row.append(_skills(row_info["skills"]))
    _row.append(len(row_info["skills"]))
    _row = _accomplishments(_row, row_info["accomplishments"])
    _row.append(__list_to_text(row_info["interests"]))
    _row.append(len(row_info["interests"]))
    return _row


def read_input_json(input_json):
    with open(input_json) as json_file:
        _full_data_list = json.load(json_file)

    raw_data_list = []
    not_found_list = []
    for _data in _full_data_list:
        if _data.__contains__("personal_info"):
            raw_data_list.append(_data)
        else:
            not_found_list.append(_data)
    return raw_data_list, not_found_list


@click.command()
@click.option("--input_json", "-i",
              default=r"../../_json_files/Graphic Designer.json",
              help="")
@click.option("--output_csv", "-o",
              default=r"../../_converted_csv/_test.csv",
              help="")
def start(input_json, output_csv):
    raw_data_list, _user_not_found_list = read_input_json(input_json)

    print("Raw Profile Size :", len(raw_data_list))
    print("Profile not Found Size :", len(_user_not_found_list))

    data_matrix = []
    for index, _data in enumerate(raw_data_list):
        data_matrix.append(create_row(_data))

    data = pd.DataFrame(data_matrix,
                        columns=["name", "headline", "company", "school", "location", "summary", "image", "followers",
                                 "email", "phone", "connected", "websites", "currentCompanyLink", "jobs", "jobSize",
                                 "education", "educationSize", "volunteering", "volunteeringSize", "skills",
                                 "skillsSize", "publications", "publicationsSize", "certifications",
                                 "certificationsSize", "patents", "patentsSize", "courses", "coursesSize", "projects",
                                 "projectsSize", "honors", "honorsSize", "testScores", "testScoresSize", "languages",
                                 "languagesSize", "organizations", "organizationsSize", "interests", "interestsSize"])
    data.to_csv(output_csv)


if __name__ == '__main__':
    start()
