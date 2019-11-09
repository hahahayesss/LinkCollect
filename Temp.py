import json
import numpy as np
import pandas as pd
from scrape_linkedin import ProfileScraper

with ProfileScraper() as scraper:
    profile = scraper.scrape(user="ahmet-turgut-8a482b96")

with open("__temp.json", "w") as _temp_file:
    json.dump(profile.to_dict(), _temp_file)
