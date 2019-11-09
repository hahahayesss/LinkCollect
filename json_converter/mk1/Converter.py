import os
import time
import json
import click
import pandas as pd


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
              default=r"../../_converted_csv/_test.json",
              help="")
def start(input_json, output_csv):
    raw_data_list, _user_not_found_list = read_input_json(input_json)

    print("Raw Profile Size :", len(raw_data_list))
    print("Profile not Found Size :", len(_user_not_found_list))

    # for _data in raw_data_list:
    #     print(_data["personal_info"]["company"])


if __name__ == '__main__':
    start()
