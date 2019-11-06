def __get_date(date_span):
    date = {}
    try:
        date["start_day"] = date_span.find_element_by_css_selector("time.date-range__start-date").text
    except:
        date["start_day"] = "unknown"

    try:
        date["duration"] = date_span.find_element_by_css_selector("span").text
    except:
        date["duration"] = "unknown"

    try:
        date["end_day"] = date_span.find_element_by_css_selector("time.date-range__end-date").text
    except:
        date["end_day"] = ""
    return date


def _from_groups(group_list):
    full_data_list = []
    for group in group_list:
        for role_data in group.find_elements_by_css_selector("li"):
            full_data_list.append({"company_name": group.find_element_by_css_selector(
                "a > div > div.experience-group-header__content > h4").text,
                                   "role_name": role_data.find_element_by_css_selector("div > h3").text,
                                   "role_date": __get_date(
                                       role_data.find_element_by_css_selector("div > div > p > span"))})
    return full_data_list


def _from_normals(normal_list):
    full_data_list = []
    for normal in normal_list:
        full_data_list.append({"company_name": normal.find_element_by_css_selector("div > h4").text,
                               "role_name": normal.find_element_by_css_selector("div > h3").text,
                               "role_date": __get_date(normal.find_element_by_css_selector("div > div > p > span"))})
    return full_data_list


class Experience:
    def __init__(self, element):
        self.element = element

    def get_data(self):
        normal_list = []
        group_list = []
        for job in self.element.find_elements_by_css_selector("li"):
            if job.get_attribute("class") == "result-card experience-item":
                normal_list.append(job)
            elif job.get_attribute("class") == "experience-group experience-item":
                group_list.append(job)
        return _from_groups(group_list) + _from_normals(normal_list)
