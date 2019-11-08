import json
import click
import pandas as pd
from scrape_linkedin import ProfileScraper

LI_AT = "AQEDAR6aCHoBhwSZAAABbkyLWfoAAAFucJfd-k0ArZHaZqjXWBbEEKGLG-PnXBn7RJTznENgkJDVL4Q2A1DfLaQU8ixioS5hgXNdQsQb6sS5blKQMhwvfqGQssdcQNBCio6klE5yXWHNBlxOmp95OfUd"


def _collect_data(profile_link):
    with ProfileScraper(cookie=LI_AT) as scraper:
        profile = scraper.scrape(user=profile_link)
    return profile.to_dict()


@click.command()
@click.option("--input_csv", "-i",
              default=r"../../csv_files/Graphic Designer.csv",
              help="")
@click.option("--output_json", "-o",
              default=r"../../json_files/Graphic Designer.json",
              help="")
def start(input_csv, output_json):
    raw_list = pd.read_csv(input_csv).values
    data_list = raw_list[:, 1]

    profile_data_list = []
    for link in data_list:
        profile_data_list.append(
            _collect_data(link.rsplit("/", 1)[1]))

    with open(output_json, "w") as json_file:
        json.dump(profile_data_list, json_file)


if __name__ == '__main__':
    start()
