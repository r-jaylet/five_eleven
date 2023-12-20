import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
import re as re
import time

browser = webdriver.Chrome()


def connect_five(browser, username: str, password: str) -> str:
    """Connect to Five website and log in using the provided credentials.

    Parameters
    ----------
    browser : selenium.webdriver.remote.webdriver.WebDriver
        An instance of the Selenium WebDriver used for browser automation.
    username : str
        The Five username for login.
    password : str
        The Five password for login.

    Returns
    -------
    str
        Returns 'Connected' if the login is successful, 'Failed' otherwise.
    """

    url = 'https://www.lefive.fr/reservations/slots'
    browser.get(url)

    # Wait for the page to load
    time.sleep(1)

    try:
        browser.find_element(By.ID, "email").send_keys(username)
        browser.find_element(By.ID, "password").send_keys(password)
        # Find and click the login button
        browser.find_element(
            By.XPATH, '//*[@id="__layout"]/div/div[1]/div[5]/div[2]/div/form/div[3]/button').click()
        return 'Connected'

    except Exception as e:
        print(f"An error occurred: {e}")
        return 'Failed'


def get_slots_results(browser, upcoming_days: int) -> list:
    """Retrieve slot results from the Five website for the specified upcoming days.

    Parameters
    ----------
    browser : selenium.webdriver.remote.webdriver.WebDriver
        An instance of the Selenium WebDriver used for browser automation.
    upcoming_days : int
        The number of upcoming days for which slot results should be retrieved.

    Returns
    -------
    list
        A list containing slot information for the selected days
    """
    results = []

    for i in range(1, upcoming_days):

        print(f"day {i}")
        try:
            # select date
            time.sleep(5)
            browser.find_element(
                By.XPATH, f'/html/body/div[1]/div/div/div[1]/div[4]/div[1]/div[1]/div[2]/div/div/div/div[{i}]').click()

            # select night slots
            time.sleep(5)
            browser.find_element(
                By.XPATH, '//*[@id="__layout"]/div/div[1]/div[5]/div[1]/div[2]/div[4]').click()

            # get slots list
            time.sleep(5)
            elements = browser.find_elements(
                By.XPATH, '//*[@id="__layout"]/div/div[1]/div[5]/div[2]/div/div')
            # extract useful info
            for e in elements:
                for line in e.text.split('\n'):
                    if line.split(' ')[0] in ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']:
                        print(line)
                        results.append(line.split(' '))
        except:
            pass

    return results


def format_slots_results(results: list, hours_to_check: list, days_to_check: list) -> pd.DataFrame:
    """Format slot results into a DataFrame and filter based on specified hours and days.

    Parameters
    ----------
    results : list
        A list containing slot information. Each item in the list is a list of strings
        representing the extracted information for each slot.
    hours_to_check : list
        A list of strings representing the hours to filter for in the results.
    days_to_check : list
        A list of strings representing the days to filter for in the results.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing formatted slot information
    """
    df = pd.DataFrame(results)
    format_df = df[[0, 1, 2, 4, 6, 7]].rename(
        columns={0: 'day',  1: 'day_num', 2: 'month', 4: 'time', 6: 'city', 7: 'arr'})
    selected_format_df = format_df.loc[(format_df['time'].isin(
        hours_to_check)) & (format_df['day'].isin(days_to_check))]

    return selected_format_df
