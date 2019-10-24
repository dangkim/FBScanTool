import calendar
import os
import platform
import sys
import urllib.request
import time
import json
import requests

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# -------------------------------------------------------------
# -------------------------------------------------------------
tokenResponse = requests.post('http://bdo8.com/connect/token', verify=False, data={
    'grant_type': 'password', 'username': 'admin', 'password': '@Bcd1234', 'client_id': 'kolviet', 'client_secret': 'kolviet'
}, headers={'Content-Type': 'application/x-www-form-urlencoded', }
)

# Global Variables

driver = None

# whether to download photos or not
download_uploaded_photos = True
download_friends_photos = False

# whether to download the full image or its thumbnail (small size)
# if small size is True then it will be very quick else if its false then it will open each photo to download it
# and it will take much more time
friends_small_size = True
photos_small_size = False

total_scrolls = 20
current_scrolls = 0
scroll_time = 10

old_height = 0

json_string = '{"ContentItemId":"","ContentItemVersionId":"","ContentType":"Influencer","DisplayText":"","Latest":true,"Published":true,"ModifiedUtc":"","PublishedUtc":"","CreatedUtc":"","Owner":"admin","Author":"ribisachi","Influencer":{"Description":{"Text":""},"Photo":{"Paths":[],"Urls":[]},"Fanpage":{"Text":""},"Email":{"Text":""},"password":{"Text":""},"FullName":{"Text":""},"ShareLink":{"Text":""},"PostImage":{"Text":""},"LiveStream":{"Text":""},"CheckIn":{"Text":""},"Video":{"Text":""},"Phone":{"Text":""},"NumberOfLike":{"Text":""},"NumberOfComment":{"Text":""},"NumberOfLove":{"Text":""},"NumberOfShare":{"Text":""},"NumberOfReaction":{"Text":""},"VideoLink":{"Paths":[]},"NumberOfPost":{"Value":0},"NumberOfFollowers":{"Value":0}},"TitlePart":{"Title":""},"MyCustomPart":{"NumberOfComment":{"Text":""}},"AgeDemorgraphic":{"Percentage":{"Text":""},"AgeGraphicsName":{"Text":""},"AgePercentage":{"Text":""}},"GenderDemorgraphic":{"GenderPercentage":{"Text":""},"GenderGraphicName":{"Text":""}},"GeoDemorgraphic":{"GeoPercentage":{"Text":""},"GeoGraphicName":{"Text":""}},"Post1":{"Time":{"Text":""},"Type":{"Text":""},"Title":{"Text":""},"Status":{"Text":""},"NumberOfComment":{"Text":""},"NumberOfShare":{"Text":""},"NumberOfReaction":{"Text":""},"Link":{"Text":""}},"Post2":{"Time":{"Text":""},"Type":{"Text":""},"Title":{"Text":""},"Status":{"Text":""},"NumberOfComment":{"Text":""},"NumberOfShare":{"Text":""},"NumberOfReaction":{"Text":""},"Link":{"Text":""}},"Post3":{"Time":{"Text":""},"Type":{"Text":""},"Title":{"Text":""},"Status":{"Text":""},"NumberOfComment":{"Text":""},"NumberOfShare":{"Text":""},"NumberOfReaction":{"Text":""},"Link":{"Text":""}},"Post4":{"Time":{"Text":""},"Type":{"Text":""},"Title":{"Text":""},"Status":{"Text":""},"NumberOfComment":{"Text":""},"NumberOfShare":{"Text":""},"NumberOfReaction":{"Text":""},"Link":{"Text":""}},"Post5":{"Time":{"Text":""},"Type":{"Text":""},"Title":{"Text":""},"Status":{"Text":""},"NumberOfComment":{"Text":""},"NumberOfShare":{"Text":""},"NumberOfReaction":{"Text":""},"Link":{"Text":""}}}'

influencerObject = json.loads(json_string)

videoModel = {
    "contentItemId": "",
    "videoPaths": [],
}

# ----------------------------------------------------------------------------


def getNumberFromThousand(x):
    if not x:
        return 0
    numberOfValue = x.lower().rsplit('k', 1)
    if len(numberOfValue) > 1:
        return float(numberOfValue[0]) * 1000
    else:
        return float(numberOfValue[0])


def getThoundsandFromNumber(x):
    if x >= 1100:
        stringValue = str(x/1000) + 'k'
        return stringValue
    else:
        return str(x)


def get_status(x):
    status = ""
    try:
        status = x.find_element_by_xpath(
            ".//div[@data-testid='post_message']").text
    except:
        try:
            status = x.find_element_by_xpath(
                ".//div[@data-testid='post_message']").text
        except:
            pass
    return status


def get_title_links(title):
    l = title.find_elements_by_tag_name('a')
    return l[-1].text, l[-1].get_attribute('href')


def get_div_links(x, tag):
    try:
        temp = x.find_element_by_xpath(".//div[@class='_3x-2']")
        return temp.find_element_by_tag_name(tag)
    except:
        return ""


def get_title(x):
    title = ""
    try:
        title = x.find_element_by_xpath(".//span[@class='fwb fcg']")
    except:
        try:
            title = x.find_element_by_xpath(".//span[@class='fcg']")
        except:
            try:
                title = x.find_element_by_xpath(".//span[@class='fwn fcg']")
            except:
                pass
    finally:
        return title


def get_time(x):
    time = ""
    try:
        time = x.find_element_by_tag_name('abbr').get_attribute('title')
        time = str("%02d" % int(time.split(", ")[1].split()[1]), ) + "-" + str(
            ("%02d" % (int((list(calendar.month_abbr).index(time.split(", ")[1].split()[0][:3]))),))) + "-" + \
            time.split()[3] + " " + str("%02d" % int(time.split()[5].split(":")[0])) + ":" + str(
            time.split()[5].split(":")[1])
    except:
        pass

    finally:
        return time


def get_reaction(x):
    reaction = ""
    try:
        reaction = x.find_element_by_xpath(".//span[@class='_81hb']")
    except:
        try:
            reaction = x.find_element_by_xpath(".//span[@class='_81hb']")
        except:
            try:
                reaction = x.find_element_by_xpath(".//span[@class='_81hb']")
            except:
                pass
    finally:
        return reaction


def get_commentno(x):
    commentno = ""
    try:
        commentno = x.find_element_by_xpath(".//span[@class='_1whp _4vn2']")
    except:
        try:
            commentno = x.find_element_by_xpath(
                ".//span[@class='_1whp _4vn2']")
        except:
            try:
                commentno = x.find_element_by_xpath(
                    ".//span[@class='_1whp _4vn2']")
            except:
                pass
    finally:
        return commentno


def get_share(x):
    share = ""
    try:
        share = x.find_element_by_xpath(".//span[@class='_355t _4vn2']")
    except:
        try:
            share = x.find_element_by_xpath(".//span[@class='_355t _4vn2']")
        except:
            try:
                share = x.find_element_by_xpath(
                    ".//span[@class='_355t _4vn2']")
            except:
                pass
    finally:
        return share

# -----------------------------------------------------------------------------


def scrape_data(id, scan_list, section, elements_path, save_status, file_names):
    """Given some parameters, this function can scrap friends/photos/videos/about/posts(statuses) of a profile"""
    page = []
    folder = os.path.join(os.getcwd(), "Data")
    username = id.split('/')[-1]

    if save_status == 4:
        page.append(id)

    for i in range(len(section)):
        page.append(id + section[i])

    for i in range(len(scan_list)):
        try:
            driver.get(page[i])

            data = driver.find_elements_by_xpath(elements_path[i])

            if len(data) > 5:
                save_to_file(file_names[i], data[0:5],
                             save_status, scan_list[i])
            else:
                save_to_file(file_names[i], data, save_status, scan_list[i])

        except:
            print("Exception (scrape_data)", str(i), "Status =",
                  str(save_status), sys.exc_info()[0])

# -----------------------------------------------------------------------------


def create_original_link(url):
    if url.find(".php") != -1:
        original_link = "https://en-gb.facebook.com/" + ((url.split("="))[1])

        if original_link.find("&") != -1:
            original_link = original_link.split("&")[0]

    elif url.find("fnr_t") != -1:
        original_link = "https://en-gb.facebook.com/" + \
            ((url.split("/"))[-1].split("?")[0])
    elif url.find("_tab") != -1:
        original_link = "https://en-gb.facebook.com/" + \
            (url.split("?")[0]).split("/")[-1]
    else:
        original_link = url

    return original_link


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def create_folder(folder):
    if not os.path.exists(folder):
        os.mkdir(folder)

# -------------------------------------------------------------
# -------------------------------------------------------------


def check_height():
    new_height = driver.execute_script("return document.body.scrollHeight")
    return new_height != old_height

# -----------------------------------------------------------------------------


def save_to_file(name, elements, status, current_section):
    """helper function used to save links to files"""
    # status 4 = dealing with posts
    results = []

    videoLinks = []

    try:
        # dealing with Videos
        if status == 2:

            if current_section == "All Videos":
                results = elements
                listOfTagA = results[0].get_attribute('href')
                if listOfTagA != '':
                    results = [x.get_attribute('href') for x in results]
                else:
                    results = [x.find_element_by_css_selector(
                        'a').get_attribute('href') for x in results]

            else:
                results = elements[0].find_elements_by_css_selector('li')
                results = [x.find_element_by_css_selector(
                    'a').get_attribute('href') for x in results]

            try:
                if results[0][0] == '/':
                    results = [r.pop(0) for r in results]
                    results = [("https://en-gb.facebook.com/" + x)
                               for x in results]
            except:
                pass

        if status == 2:
            index = 0
            for x in results:
                index += 1
                if index > 10:
                    break
                videoLinks.append(x)

            videoModel["videoPaths"] = videoLinks

    except:
        print("Exception (save_to_file)", "Status =",
              str(status), sys.exc_info()[0])

    return

# -----------------------------------------------------------------------------

# helper function: used to scroll the page


def scroll():
    global old_height
    current_scrolls = 0

    while (True):
        try:
            if current_scrolls == total_scrolls:
                return

            old_height = driver.execute_script(
                "return document.body.scrollHeight")
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            WebDriverWait(driver, scroll_time, 0.05).until(
                lambda driver: check_height())
            current_scrolls += 1
        except TimeoutException:
            break

    return


# A simple function to use requests.post to make the API call. Note the json= section.
def run_query(query):

    # get influencer by userName
    tokenObject = json.loads(tokenResponse.content)
    tokenAuthorization = tokenObject['token_type'] + \
        " " + tokenObject['access_token']

    request = requests.post('http://bdo8.com/api/graphql', json={'query': query}, headers={
        'Authorization': tokenAuthorization})

    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(
            request.status_code, query))


def scrap_profile(ids):
    folder = os.path.join(os.getcwd(), "Data")
    create_folder(folder)
    os.chdir(folder)
    urls = []
    userNames = []
    # execute for all profiles given in input.txt file
    for id in ids:
        driver.get(id)
        originalUrl = str(driver.current_url)
        url = originalUrl.rstrip('/')
        id = create_original_link(url)

        userName = id.rsplit('/')[-1]

        # The GraphQL query (with a few aditional bits included) itself defined as a multi-line string.
        query = '''{{
	        influencer(where: {{displayText_contains: "{0}"}}, status: PUBLISHED) {{
                contentItemId
            }} 
        }}'''.format(userName)

        result = run_query(query)  # execute query

        videoModel['contentItemId'] = result['data']['influencer'][0]['contentItemId']

        print("\nScraping:", id)

        # ----------------------------------------------------------------------------
        print("----------------------------------------")
        print("Videos:")
        # setting parameters for scrape_data() to scrap videos
        # scan_list = ["'s Videos", "Videos of"]
        # section = ["/videos_by", "/videos_of"]
        # elements_path = [
        #     "//*[contains(@id, 'pagelet_timeline_app_collection_')]/ul"] * 2

        try:
            followerSpan = driver.find_element_by_xpath(
                "//*[@id='profileEscapeHatchContentID']/div[2]/div/div[2]/div[2]/div[2]/span")
            scan_list = ["'s Videos"]
            section = ["/videos_by"]
            elements_path = [
                "//*[contains(@id, 'pagelet_timeline_app_collection_')]/ul"]
            file_names = ["Uploaded Photos.txt", "Tagged Photos.txt"]
        except NoSuchElementException:
            try:
                followerSpan = driver.find_element_by_xpath(
                    "//*[@id='entity_sidebar']/div[2]/div[2]/div")
                scan_list = ["All Videos"]
                section = ["/videos"]
                elements_path = [
                    "//*[contains(@class, '_3vwb _400z _2-40')]"]
                file_names = ["Uploaded Photos.txt", "Tagged Photos.txt"]
            except NoSuchElementException:
                scan_list = ["All Videos"]
                section = ["/videos"]
                elements_path = [
                    "//*[contains(@class, '_3v4h _48gm _50f3 _50f7')]"]
                file_names = ["Uploaded Photos.txt", "Tagged Photos.txt"]

        save_status = 2

        scrape_data(id, scan_list, section, elements_path,
                    save_status, file_names)
        print("Videos Done!")
        # ----------------------------------------------------------------------------

    tokenObject = json.loads(tokenResponse.content)
    tokenAuthorization = tokenObject['token_type'] + \
        " " + tokenObject['access_token']

    videoModelJson = json.dumps(videoModel)

    influencerResponse = requests.post('http://bdo8.com/api/content/UpdateVideos', verify=False, data=videoModelJson, headers={
                                       'Content-Type': 'application/json', 'Authorization': tokenAuthorization})

    print("\nProcess Completed.")

    # ----------------------------------------------------------------------------

    return


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

def safe_find_element_by_id(driver, elem_id):
    try:
        return driver.find_element_by_id(elem_id)
    except NoSuchElementException:
        return None


def login(email, password):
    """ Logging into our own profile """

    try:
        global driver

        options = Options()

        #  Code to disable notifications pop up of Chrome Browser
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--mute-audio")
        # options.add_argument("headless")

        try:
            platform_ = platform.system().lower()
            if platform_ in ['linux', 'darwin']:
                driver = webdriver.Chrome(
                    executable_path="./chromedriver", options=options)
            else:
                driver = webdriver.Chrome(
                    executable_path="./chromedriver.exe", options=options)
        except:
            print("Kindly replace the Chrome Web Driver with the latest one from "
                  "http://chromedriver.chromium.org/downloads "
                  "and also make sure you have the latest Chrome Browser version."
                  "\nYour OS: {}".format(platform_)
                  )
            exit()

        driver.get("https://en-gb.facebook.com")
        driver.maximize_window()

        # filling the form
        driver.find_element_by_name('email').send_keys(email)
        driver.find_element_by_name('pass').send_keys(password)

        # clicking on login button
        driver.find_element_by_id('loginbutton').click()

        # if your account uses multi factor authentication
        mfa_code_input = safe_find_element_by_id(driver, 'approvals_code')

        if mfa_code_input is None:
            return

        mfa_code_input.send_keys(input("Enter MFA code: "))
        driver.find_element_by_id('checkpointSubmitButton').click()

        # there are so many screens asking you to verify things. Just skip them all
        while safe_find_element_by_id(driver, 'checkpointSubmitButton') is not None:
            dont_save_browser_radio = safe_find_element_by_id(driver, 'u_0_3')
            if dont_save_browser_radio is not None:
                dont_save_browser_radio.click()

            driver.find_element_by_id('checkpointSubmitButton').click()

    except Exception as e:
        print("There's some error in log in.")
        print(sys.exc_info()[0])
        exit()


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

def main():
    with open('C:\\ScraperVideoOnly\\credentials.txt') as f:
        email = f.readline().split('"')[1]
        password = f.readline().split('"')[1]

        if email == "" or password == "":
            print(
                "Your email or password is missing. Kindly write them in credentials.txt")
            exit()

    ids = ["https://en-gb.facebook.com/" + line.split("/")[-1] for line in open(
        "C:\\ScraperVideoOnly\\input.txt", newline='\n')]

    if len(ids) > 0:
        print("\nStarting Scraping...")

        login(email, password)
        scrap_profile(ids)
        driver.close()
    else:
        print("Input file is empty.")


# -------------------------------------------------------------
# -------------------------------------------------------------
# -------------------------------------------------------------

if __name__ == '__main__':
    # get things rolling
    main()
