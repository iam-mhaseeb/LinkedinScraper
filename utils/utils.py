import json
from time import sleep

from selenium import webdriver

from validator_collection import checkers


def load_config(path):
    """
    Load configuration file with all the needed parameters

    :param path: str path of the conf file
    :return: dict
    """
    with open(path, 'r') as conf_file:
        conf = json.load(conf_file)
    return conf


def init_driver(chrome_path, chromedriver_path):
    """
    Iniitialize Chrome driver
    :param chrome_path: str chrome executable path
    :param chromedriver_path: str chrome driver path
    :return: selenium driver object
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = chrome_path
    chrome_options.add_argument("--normal")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-infobars")
    driver = webdriver.Chrome(executable_path=chromedriver_path,
                              chrome_options=chrome_options)
    return driver


def login(driver, user, pwd):
    """
    Type user email and password in the relevant fields and
    perform log in on linkedin.com by using the given credentials.

    :param driver: selenium chrome driver object
    :param user: str username, email
    :param pwd: str password
    :return: None
    """
    username = driver.find_element_by_id('username')
    username.send_keys(user)
    sleep(0.5)
    password = driver.find_element_by_id('password')
    password.send_keys(pwd)
    sleep(0.5)
    sign_in_button = driver.find_element_by_class_name('btn__primary--large')
    sign_in_button.click()


def get_profile_urls(driver, n_pages=1):
    """
    Return a list without repetitions of alphabetically sorted URLs
    taken from the results of a given query on Google search.

    :param driver: selenium chrome driver object
    :param n_pages: int number of google pages to loop over
    :return: list of linkedin-profile URLs
    """
    linkedin_urls = []

    for i in range(n_pages):
        urls = driver.find_elements_by_css_selector('#search a')
        linkedin_urls += [url.get_attribute('href') for url in urls
                          if checkers.is_url(url.get_attribute('href'))]
        sleep(2)

        if i > 1:
            try:
                next_button_url = driver.find_element_by_css_selector(
                    '#pnnext').get_attribute('href')
                driver.get(next_button_url)
            except NoSuchElementException:
                break

    linkedin_urls_no_rep = sorted(list(dict.fromkeys([url for url in linkedin_urls])))
    return linkedin_urls_no_rep


def get_unseen_urls(collection, urls):
    """
    Get a list of URLs that have not already been scraped.
    Loop over all the db entries and create a list with the
    URLs already scraped.
    Get the difference of such list and the list of all the URLs
    for a given query.
    Return a list of URLs which have not already been scraped.

    :param collection: Scrapped data
    :param urls: lsit of URLs to check
    :return: list of unseen URLs
    """
    scraped_urls = [entry.get("URL") for entry in collection]
    unseen_urls = list(set(urls) - set(scraped_urls))
    return unseen_urls


def print_scraped_data(data):
    """
    Print the user data returned by scrape_url().

    """
    print()
    for key in data:
        print(key + ": " + str(data[key]))


def load_data(filepath):
    """
    Loads data from json file to system

    :param filepath: Path of json file
    :return: Scrapped data
    """

    with open(filepath, "r+") as f:
        return json.loads(f.read())


def write_data(filepath, data):
    """
    Write data to json file from system

    :param filepath: Path of json file
    :param data: Scrapped data
    :return: None
    """

    with open(filepath, "w+") as f:
        f.write(json.dumps(data))
