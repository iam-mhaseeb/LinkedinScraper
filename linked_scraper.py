import sys
import argparse
from time import sleep

from utils.utils import (
    get_profile_urls,
    get_unseen_urls,
    init_driver,
    load_config,
    load_data,
    login,
    print_scraped_data,
    write_data
)

from user_scrapper.user_scrapper import UserScraper

from selenium.webdriver.common.keys import Keys

CONFIG_FILE_PATH = 'config.json'
DATA_FILE_PATH = 'scrapped_data.json'


def user_scrapper(conf):
    """
    Calls user scrapper & manage data movement
    :param conf: str configuration dict
    """
    scrapped_data = [] or load_data(DATA_FILE_PATH)
    driver = init_driver(conf['parameters']['CHROME_PATH'], conf['parameters']['CHROMEDRIVER_PATH'])
    driver.get("https://www.linkedin.com")
    sleep(0.5)
    driver.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
    login(driver, conf['credentials']['LINUSERNAME'], conf['credentials']['LINPWD'])
    # scraper = UserScraper(driver)

    for query in conf['USER_QUERIES']:
        driver.get("https://www.google.com")
        sleep(2)
        search_query = driver.find_element_by_name('q')

        try:
            search_query.send_keys(query)
        except ElementNotInteractableException:
            print("ERROR :: Cannot send query. Google might be blocking")
            sys.exit(1)

        sleep(0.5)
        search_query.send_keys(Keys.RETURN)
        profile_urls = get_profile_urls(driver)

        if len(profile_urls) == 0:
            print("\n\n")
            print("WARNING :: Could not get any URLs for the query\n" + query)
            print("Please double-check that Google is not blocking the query")
            print("\n\n")
            continue

        unseen_urls = get_unseen_urls(scrapped_data, profile_urls)

        if len(unseen_urls) != 0:
            print("INFO :: Resuming from URL", unseen_urls[0])
        else:
            print("INFO :: All URLs from Google-search page(s) for the query " + query + " have already been scraped. Moving onto the next query if any.")
            continue

        for url in unseen_urls:
            # user_data = scraper.scrape_user(query, url)
            user_data = {}
            if user_data:
                print_scraped_data(user_data)
                scrapped_data.append(user_data)
                write_data(DATA_FILE_PATH, scrapped_data)

    driver.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['user', 'job'], help='Choose mode of scrapper')
    args = parser.parse_args()
    conf = load_config(CONFIG_FILE_PATH)
    if args.mode == 'user':
        user_scrapper(conf)
    elif args.mode == 'job':
        raise NotImplementedError('This functionality is not available yet.')
