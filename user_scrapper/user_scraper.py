from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from bs4 import BeautifulSoup as bs


class UserScraper:
    def __init__(self, driver):
        """
        Initialize the class

        :param driver: selenium chrome driver object
        """
        self.driver = driver

    def get_name(self):
        """
        Get the name of the user whose profile page is being scraped.

        :param soup: BeautifulSoup object
        :return: name: str name of the user
        """
        soup = bs(self.driver.page_source, 'html.parser')
        try:
            name_tag = soup.find_all(class_="t-24")[0]
            name = name_tag.get_text(strip=True)
            return name
        except IndexError:
            return ""

    def get_job_title(self):
        """
        Get the job title of the user whose profile
        page is being scraped

        :param soup: BeautifulSoup object
        :return: job_title: str
        """
        soup = bs(self.driver.page_source, 'html.parser')
        try:
            job_title_tag = soup.find_all(class_="t-18")[0]
            job_title = job_title_tag.get_text(strip=True)
            return job_title
        except IndexError:
            return ""

    def get_location(self):
        """
        Get the location of the user whose profile
        page is being scraped.

        :param soup: BeautifulSoup object
        :return: location: str
        """
        soup = bs(self.driver.page_source, 'html.parser')
        try:
            location_tag = soup.select("li.t-16.t-black.t-normal.inline-block")
            location = location_tag[0].get_text(strip=True) if location_tag else ''
            return location
        except IndexError:
            return ""

    def get_degree(self):
        """
        Get the all education data of the user whose profile page
        is being scraped.

        :param soup: BeautifulSoup object
        :return: education_data: dict
        """
        soup = bs(self.driver.page_source, 'html.parser')
        education_data = []
        degree_elems = soup.select("li.pv-education-entity")

        element = self.driver.find_element_by_css_selector("li.pv-education-entity")
        ActionChains(self.driver).move_to_element(element).perform()

        if len(degree_elems) != 0:

            for elem in degree_elems:
                school_name = elem.select("h3.pv-entity__school-name")[0].get_text(strip=True) if elem.select("h3.pv-entity__school-name") else ''
                degree_name = elem.select("p.pv-entity__degree-name")[0].get_text(strip=True) if elem.select("p.pv-entity__degree-name") else ''
                dates = elem.select("p.pv-entity__dates")[0].get_text(strip=True) if elem.select("p.pv-entity__dates") else ''

                education_data.append({
                    "school_name": school_name,
                    "degree_name": degree_name,
                    "dates": dates
                })

        return education_data

    def get_experience(self):
        """
        Get the all experience data of the user whose profile page
        is being scraped.

        :param soup: BeautifulSoup object
        :return: experience_data: dict
        """
        soup = bs(self.driver.page_source, 'html.parser')
        experience_data = []
        experience_elems = soup.select("li.v-entity__position-group-pager")

        element = self.driver.find_element_by_css_selector("li.v-entity__position-group-pager")
        ActionChains(self.driver).move_to_element(element).perform()

        if len(experience_elems) != 0:

            for elem in experience_elems:
                job_title = elem.select("h3")[0].get_text(strip=True) if elem.select("h3") else ''
                company_name = elem.select("p.pv-entity__secondary-title")[0].get_text(strip=True) if elem.select("p.pv-entity__secondary-title") else ''
                dates = elem.select("h4.pv-entity__date-range")[0].get_text(strip=True) if elem.select("h4.pv-entity__date-range") else ''
                duration = elem.select("span.pv-entity__bullet-item-v2")[0].get_text(strip=True) if elem.select("span.pv-entity__bullet-item-v2") else ''
                location = elem.select("h4.pv-entity__location")[0].get_text(strip=True) if elem.select("h4.pv-entity__location") else ''

                experience_data.append({
                    "job_title": job_title,
                    "company_name": company_name,
                    "dates": dates,
                    "duration": duration,
                    "location": location
                })

        return experience_data

    def get_skills(self):
        """
        Get the skills of the user whose profile page is being scraped.
        Return a list of skills.

        :return: list: skills
        """
        skills = []

        element = self.driver.find_element_by_css_selector("button.pv-skills-section__additional-skills")
        ActionChains(self.driver).move_to_element(element).perform()

        sleep(5)
        # wait for button to appear
        wait = WebDriverWait(self.driver, 20)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.pv-skills-section__additional-skills")))
        # Click on contact info button
        self.driver.find_element_by_css_selector("button.pv-skills-section__additional-skills").click()
        sleep(5)
        # wait for dialog to show
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.pv-skill-categories-section__expanded")))

        soup = bs(self.driver.page_source, 'html.parser')
        skills_tags = soup.find_all(class_="pv-skill-category-entity__name-text")
        skills = [item.get_text(strip=True) for item in skills_tags]
        skills = [skill for skill in skills if skill]

        return skills

    def get_languages(self):
        """
        Get the languages in the "Accomplishments" section
        of the user whose profile page is being scraped.
        Look for the accomplishment tags first, and get all the language
        elements from them.
        Return a list of languages.

        :param soup: BeautifulSoup object
        :return: list: languages list
        """
        soup = bs(self.driver.page_source, 'html.parser')
        languages = []
        languages_elements = soup.select("div.languages-expandable-content")

        element = self.driver.find_element_by_css_selector("div.languages-expandable-content")
        ActionChains(self.driver).move_to_element(element).perform()

        for elem in languages_elements:
            langage = elem.select("li")[0].get_text(strip=True) if elem.select("li") else ''

            if langage:
                languages.append(langage)

        return languages

    def get_contact_info(self):
        """
        Get the public contact info of a profile.
        Return a dict of contact info.

        :param soup: BeautifulSoup object
        :return: dict: contact info
        """
        contact_info = {
            "phone_number": "",
            "email": "",
            "linkedin": "",
            "twitter": "",
            "websites": "",
            "birthday": "",
        }
        sleep(10)
        # wait for button to appear
        wait = WebDriverWait(self.driver, 20)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "ul.pv-top-card--list-bullet a.ember-view")))
        # Click on contact info button
        self.driver.find_element_by_css_selector("ul.pv-top-card--list-bullet a.ember-view").click()
        sleep(10)
        # wait for dialog to show
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.artdeco-modal--layer-default")))

        soup = bs(self.driver.page_source, 'html.parser')

        contact_info_element = soup.select("div.artdeco-modal--layer-default")
        contact_info['twitter'] = soup.select("section.ci-twitter a")[0]["href"] if soup.select("section.ci-twitter a") else ''
        contact_info['websites'] = soup.select("section.ci-websites a")[0]["href"] if soup.select("section.ci-websites a") else ''
        contact_info['linkedin'] = soup.select("section.ci-vanity-url a")[0]["href"] if soup.select("section.ci-vanity-url a") else ''
        contact_info['email'] = soup.select("section.ci-email a")[0]["href"] if soup.select("section.ci-email a") else ''
        contact_info['birthday'] = soup.select("section.ci-birthday span")[0].get_text(strip=True) if soup.select("section.ci-birthday span") else ''

        self.driver.find_element_by_css_selector("button.artdeco-modal__dismiss").click()
        sleep(10)

        return contact_info

    def scrape_user(self, query, url):
        """
        Get the user data for a given query and linkedin URL.
        Call get_name() and get_job_title() to get name and
        job title, respectively. Scroll down the given URL
        to make the skill-section HTML code appear;
        call get_skills() and get_degree() to extract the user skills
        and their degree, respectively. Scroll down the page until its
        end to extract the user languages by calling
        get_languages().
        Finally, return a dictionary with the extracted data.

        :param query: str
        :param url: str URL to scrape
        :return:
        """
        attempt = 0
        max_attempts = 3
        success = False
        user_data = {}
        while not success:
            try:
                attempt += 1
                self.driver.get(url)
                sleep(2)
                contact_info = self.get_contact_info()
                sleep(3)
                name = self.get_name()
                job_title = self.get_job_title()
                location = self.get_location()
                experience = self.get_experience()
                degree = self.get_degree()
                skills = self.get_skills()
                languages = self.get_languages()
                user_data = {
                    "URL": url,
                    "name": name,
                    "query": query,
                    "job_title": job_title,
                    "degree": degree,
                    "experience": experience,
                    "location": location,
                    "languages": languages,
                    "skills": skills,
                    "contact_info": contact_info
                }
                success = True
            except TimeoutException:
                print("\nINFO :: TimeoutException raised while " +
                      "getting URL\n" + url)
                print("INFO :: Attempt n." + str(attempt) + " of " +
                      str(max_attempts) +
                      "\nNext attempt in 60 seconds")
                sleep(60)
            if success:
                break
            if attempt == max_attempts and not user_data:
                print("INFO :: Max number of attempts reached. " +
                      "Skipping URL" +
                      "\nUser data will be empty.")
        return user_data
