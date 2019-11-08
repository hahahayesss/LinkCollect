def _get_volunteer_data(volunteer_job):
    volunteer_data = {"title": volunteer_job.find_element_by_css_selector("div > h3").text,
                      "subtitle": volunteer_job.find_element_by_css_selector("div > h4").text}
    try:
        volunteer_data["start_date"] = volunteer_data.find_element_by_css_selector(
            "div > div > p > span > time.date-range__start-date").text
    except:
        volunteer_data["start_date"] = "unknown"

    try:
        volunteer_data["end_date"] = volunteer_data.find_element_by_css_selector(
            "div > div > p > span > time.date-range__end-date").text
    except:
        volunteer_data["end_date"] = "unknown"
    return volunteer_data


class Volunteer:
    def __init__(self, element):
        self.element = element

    def get_data(self):
        volunteer_list = []
        for volunteer_job in self.element.find_elements_by_css_selector("li"):
            volunteer_list.append(_get_volunteer_data(volunteer_job))
        return volunteer_list
