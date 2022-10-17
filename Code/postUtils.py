from selenium.common.exceptions import NoSuchElementException
import calendar
from selenium.webdriver.common.by import By
import time


# Get Shared number
def get_share(x):
    share = ""
    try:
        share = x.find_elements(By.XPATH,
                                ".//span[@class='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x1f6kntn xvq8zen xo1l8bm xi81zsa'][2]")[
            0].get_attribute("innerHTML")
    except NoSuchElementException:
        pass
    finally:
        return share


# Get Number of Comments
def get_comment_number(x):
    comment_number = ""
    try:
        comment_number = x.find_elements(By.XPATH,
                                         ".//span[@class='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x1f6kntn xvq8zen xo1l8bm xi81zsa'][1]")[
            0].get_attribute("innerHTML")
    except NoSuchElementException:
        pass
    finally:
        return comment_number


# Get Reactive
def get_reactive(x):
    reactive = ""
    try:
        reactive = x.find_elements(By.XPATH, ".//span[@class='x16hj40l']")[0].get_attribute("innerHTML")
    except NoSuchElementException:
        pass
    finally:
        return reactive


# Get Post Title
def get_title(x):
    title = ""
    try:
        title = x.find_elements(By.XPATH, ".//div[@class='xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs x126k92a']")[0].text
        test = 1
    except NoSuchElementException:
        pass
    finally:
        return title


# Get Post's status
def get_status(x):
    status = ""
    try:
        status = ""
    except NoSuchElementException:
        pass
    return status


# Get Post Time
def get_time(x):
    post_time = ""
    try:
        post_time = ""
    except NoSuchElementException:
        pass
    finally:
        return post_time
