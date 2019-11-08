def _get_education_data(education_data):
    school_data = {"school_name": education_data.find_element_by_css_selector("div > h3").text,
                   "school_department": education_data.find_element_by_css_selector("div > h4").text}

    try:
        school_data["start_date"] = education_data.find_element_by_css_selector(
            "div > div > p > span > time.date-range__start-date").text
    except:
        school_data["start_date"] = "unknown"

    try:
        school_data["end_date"] = education_data.find_element_by_css_selector(
            "div > div > p > span > time.date-range__end-date").text
    except:
        school_data["end_date"] = "unknown"
    return school_data


class Education:
    def __init__(self, element):
        self.element = element

    def get_data(self):
        education_list = []
        for education_data in self.element.find_elements_by_css_selector("li"):
            education_list.append(_get_education_data(education_data))
        return education_list
