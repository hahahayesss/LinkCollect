import os
import time
import json
import click
import send2trash
import pandas as pd
from scrape_linkedin import ProfileScraper

LI_AT = ""


def _collect_data(profile_link):
    try:
        with ProfileScraper(cookie=LI_AT) as scraper:
            profile = scraper.scrape(user=profile_link)
        return profile.to_dict()
    except:
        return {"notFound": True, "userLink": profile_link}


def _write_temp_file(_temp_list, _temp_folder):
    if not os.path.exists(_temp_folder):
        os.mkdir(_temp_folder)

    _temp_file_name = str(time.time()) + ".q"
    with open(os.path.join(_temp_folder, _temp_file_name), "w") as _temp_file:
        json.dump(_temp_list, _temp_file)


def _write_output(output, _temp_folder):
    _temp_files = [f for f in os.listdir(_temp_folder) if f.__contains__(".q")]
    _temp_list = []
    for _temp in _temp_files:
        with open(os.path.join(_temp_folder, _temp)) as _temp_file:
            _temp_list += json.load(_temp_file)

    with open(output, "w") as json_file:
        json.dump(_temp_list, json_file)

    send2trash.send2trash(_temp_folder)


@click.command()
@click.option("--input_csv", "-i",
              default=r"../../csv_files/Graphic Designer.csv",
              help="")
@click.option("--output_json", "-o",
              default=r"../../json_files/Graphic Designer.json",
              help="")
@click.option("--temp_folder", "-t",
              default=r"_temp",
              help="")
def start(input_csv, output_json, temp_folder):
    raw_list = pd.read_csv(input_csv).values
    data_list = raw_list[:, 1]

    _process_percent_size = int(len(data_list) / 100)
    _process_counter = 0

    profile_data_list = []
    for index, link in enumerate(data_list):
        profile_data_list.append(
            _collect_data(link.rsplit("/", 1)[1]))
        if len(profile_data_list) == 10:
            _write_temp_file(profile_data_list, temp_folder)
            profile_data_list.clear()
        if index % _process_percent_size == 0:
            print("%" + str(_process_counter))
            _process_counter += 1

    _write_output(output_json, temp_folder)


if __name__ == '__main__':
    start()
