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
tokenResponse = requests.post('https://localhost:44300/connect/token', verify=False, data={
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

total_scrolls = 15
current_scrolls = 10
scroll_time = 5

old_height = 0

json_string = '{"ContentItemId":"","ContentItemVersionId":"","ContentType":"Influencer","DisplayText":"","Latest":true,"Published":true,"ModifiedUtc":"","PublishedUtc":"","CreatedUtc":"","Owner":"admin","Author":"ribisachi","Influencer":{"Description":{"Text":""},"Photo":{"Paths":[],"Urls":[]},"Fanpage":{"Text":""},"Email":{"Text":""},"password":{"Text":""},"FullName":{"Text":""},"ShareLink":{"Text":""},"PostImage":{"Text":""},"LiveStream":{"Text":""},"CheckIn":{"Text":""},"Video":{"Text":""},"Phone":{"Text":""},"NumberOfLike":{"Text":""},"NumberOfComment":{"Text":""},"NumberOfLove":{"Text":""},"NumberOfShare":{"Text":""},"NumberOfReaction":{"Text":""},"VideoLink":{"Paths":[]},"NumberOfPost":{"Value":0},"NumberOfFollowers":{"Value":0}},"TitlePart":{"Title":""},"MyCustomPart":{"NumberOfComment":{"Text":""}},"AgeDemorgraphic":{"Percentage":{"Text":""},"AgeGraphicsName":{"Text":""},"AgePercentage":{"Text":""}},"GenderDemorgraphic":{"GenderPercentage":{"Text":""},"GenderGraphicName":{"Text":""}},"GeoDemorgraphic":{"GeoPercentage":{"Text":""},"GeoGraphicName":{"Text":""}},"Post1":{"Time":{"Text":""},"Type":{"Text":""},"Title":{"Text":""},"Status":{"Text":""},"NumberOfComment":{"Text":""},"NumberOfShare":{"Text":""},"NumberOfReaction":{"Text":""},"Link":{"Text":""}},"Post2":{"Time":{"Text":""},"Type":{"Text":""},"Title":{"Text":""},"Status":{"Text":""},"NumberOfComment":{"Text":""},"NumberOfShare":{"Text":""},"NumberOfReaction":{"Text":""},"Link":{"Text":""}},"Post3":{"Time":{"Text":""},"Type":{"Text":""},"Title":{"Text":""},"Status":{"Text":""},"NumberOfComment":{"Text":""},"NumberOfShare":{"Text":""},"NumberOfReaction":{"Text":""},"Link":{"Text":""}},"Post4":{"Time":{"Text":""},"Type":{"Text":""},"Title":{"Text":""},"Status":{"Text":""},"NumberOfComment":{"Text":""},"NumberOfShare":{"Text":""},"NumberOfReaction":{"Text":""},"Link":{"Text":""}},"Post5":{"Time":{"Text":""},"Type":{"Text":""},"Title":{"Text":""},"Status":{"Text":""},"NumberOfComment":{"Text":""},"NumberOfShare":{"Text":""},"NumberOfReaction":{"Text":""},"Link":{"Text":""}}}'

influencerObject = json.loads(json_string)

followerAndPhotoModel = {
    "ContentItemId": "",
    "PhotoPaths": [],
    "NumberOfFollowers": 0
}

# ----------------------------------------------------------------------------
# -------------------------------------------------------------


def get_facebook_images_url(img_links):
    urls = []
    index = 0
    for link in img_links:
        index += 1
        if index > 5:
            break
        if link != "None":
            valid_url_found = False
            driver.get(link)

            try:
                while not valid_url_found:
                    WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "spotlight")))
                    element = driver.find_element_by_class_name("spotlight")
                    img_url = element.get_attribute('src')
                    print(img_url)
                    if img_url.find('.gif') == -1:
                        valid_url_found = True
                        urls.append(img_url)
            except:
                urls.append("None")
        else:
            urls.append("None")

    return urls


# -------------------------------------------------------------

# -----------------------------------------------------------------------------


def save_to_file(name, elements, status, current_section, username=''):
    """helper function used to save links to files"""

    # status 1 = dealing with photos

    try:
        results = []
        img_names = []

        # dealing with Photos
        # Influencer Photos
        if status == 1:
            results = [x.get_attribute('href') for x in elements]
            results.pop(0)

            try:
                if download_uploaded_photos:
                    if photos_small_size:
                        background_img_links = driver.find_elements_by_xpath(
                            "//*[contains(@id, 'pic_')]/div/i")
                        background_img_links = [x.get_attribute(
                            'style') for x in background_img_links]
                        background_img_links = [((x.split('(')[1]).split(')')[0]).strip('"') for x in
                                                background_img_links]
                    else:
                        background_img_links = get_facebook_images_url(results)

                    folder_names = ["Uploaded Photos", "Tagged Photos"]

                    img_names = image_downloader(
                        background_img_links, folder_names[current_section])

                else:
                    img_names = ["None"] * len(results)
            except:
                print("Exception (Images)", str(status), "Status =",
                      current_section, sys.exc_info()[0])

    except:
        print("Exception (save_to_file)", "Status =",
              str(status), sys.exc_info()[0])

    return

# ----------------------------------------------------------------------------
# -------------------------------------------------------------

# takes a url and downloads image from that url


def image_downloader(img_links, folder_name):
    img_names = []
    photoLinks = []
    try:
        for link in img_links:
            img_name = "None"
            if link != "None":
                img_name = (link.split('.jpg')[0]).split('/')[-1] + '.jpg'
                # img_name = username + '.jpg'
                # this is the image id when there's no profile pic
                if img_name == "10354686_10150004552801856_220367501106153455_n.jpg":
                    img_name = "None"
                else:
                    try:
                        photoLinks.append(link)
                        # urllib.request.urlretrieve(link, img_name)
                    except:
                        img_name = "None"
            img_names.append(img_name)

        # influencerObject["Influencer"]["Photo"]["Paths"] = photoLinks
        followerAndPhotoModel['PhotoPaths'] = photoLinks

        # ----------------------------------------------------------------------------

        tokenObject = json.loads(tokenResponse.content)
        tokenAuthorization = tokenObject['token_type'] + \
            " " + tokenObject['access_token']

        followerAndPhotoModelJson = json.dumps(followerAndPhotoModel)

        influencerResponse = requests.post('https://localhost:44300/api/content/UpdateFollowerAndPhoto', verify=False, data=followerAndPhotoModelJson, headers={
            'Content-Type': 'application/json', 'Authorization': tokenAuthorization})

        followerAndPhotoModel["ContentItemId"] = ''
        followerAndPhotoModel["PhotoPaths"] = []
        followerAndPhotoModel["NumberOfFollowers"] = 0

    except:
        print("Exception (image_downloader):", sys.exc_info()[0])

    return img_names

# -------------------------------------------------------------
# -------------------------------------------------------------


def scrape_data(id, scan_list, section, elements_path, save_status, file_names):
    """Given some parameters, this function can scrap friends/photos/videos/about/posts(statuses) of a profile"""
    page = []
    username = id.split('/')[-1]

    if save_status == 4:
        page.append(id)

    for i in range(len(section)):
        page.append(id + section[i])

    for i in range(len(scan_list)):
        try:
            driver.get(page[i])

            data = driver.find_elements_by_xpath(elements_path[i])

            save_to_file(file_names[i], data, save_status, i, username)

        except:
            print("Exception (scrape_data)", str(i), "Status =",
                  str(save_status), sys.exc_info()[0])


# -----------------------------------------------------------------------------
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

    request = requests.post('https://localhost:44300/api/graphql', verify=False, json={'query': query}, headers={
        'Authorization': tokenAuthorization})

    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(
            request.status_code, query))
        return {}


def scrap_profile(ids):
    urls = []
    userNames = []
    scan_list = []
    section = []
    elements_path = []
    file_names = []
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

        if len(result['data']['influencer']) > 0:

            followerAndPhotoModel['ContentItemId'] = result['data']['influencer'][0]['contentItemId']

            print("\nScraping:", id)

            try:
                followerSpan = driver.find_element_by_xpath(
                    "//*[@id='profileEscapeHatchContentID']/div[2]/div/div[2]/div[2]/div[2]/span")
                followerSpanTextList = followerSpan.text.split(' ')
                followerSpanText = followerSpanTextList[0]
                followerSpanText = followerSpanText.replace(",", "")
                followerSpanText = followerSpanText.replace(".", "")
                scan_list = ["Photos of"]
                section = ["/photos", "/photos_all", "/photos_of"]
                elements_path = ["//*[contains(@id, 'pic_')]"] * 2
                file_names = ["Uploaded Photos.txt", "Tagged Photos.txt"]
            except NoSuchElementException:
                try:
                    followerSpan = driver.find_element_by_css_selector(
                        "._4-u2._6590._3xaf._4-u8")

                    followerSpanTextList = followerSpan.text.split('\n')

                    for target_list in followerSpanTextList:
                        if "people follow this" in target_list or "người theo dõi trang này" in target_list:
                            followerSpanText = target_list.split(' ')[0]
                            if 'K' in followerSpanText:
                                followerSpanText = str(
                                    int(followerSpanText.split('K')[0]) * 1000)
                            else:
                                followerSpanText = followerSpanText.replace(
                                    ",", "")
                                followerSpanText = followerSpanText.replace(
                                    ".", "")
                        pass

                    scan_list = ["All Photos"]
                    section = ["/photos"]
                    elements_path = ["//*[contains(@class, '_2eea')]/a"]
                    file_names = ["Uploaded Photos.txt", "Tagged Photos.txt"]
                except NoSuchElementException:
                    followerSpanText = ""
                    followerSpan = driver.find_element_by_xpath(
                        "//*[@id='entity_sidebar']/div[2]/div[2]/div")
                    followerSpanTextList = followerSpan.text.split('\n')
                    for target_list in followerSpanTextList:
                        if "followers" in target_list:
                            followerSpanText = target_list.split(' ')[0]
                            if 'K' in followerSpanText:
                                followerSpanText = str(
                                    int(followerSpanText.split('K')[0]) * 1000)
                            else:
                                followerSpanText = followerSpanText.replace(
                                    ",", "")
                                followerSpanText = followerSpanText.replace(
                                    ".", "")
                        pass

                    scan_list = ["All Photos"]
                    section = ["/photos"]
                    elements_path = ["//*[contains(@class, '_2eea')]/a"]
                    file_names = ["Uploaded Photos.txt", "Tagged Photos.txt"]

            followerAndPhotoModel['NumberOfFollowers'] = int(
                followerSpanText.strip())
            print(followerSpan.text)
        # ----------------------------------------------------------------------------

        print("----------------------------------------")
        print("Photos..")
        print("Scraping Links..")
        # setting parameters for scrape_data() to scrap photos

        save_status = 1

        scrape_data(id, scan_list, section, elements_path,
                    save_status, file_names)
        print("Photos Done!")

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
    with open('C:\\ScraperFollowersAndPhotosOnly\\credentials.txt') as f:
        email = f.readline().split('"')[1]
        password = f.readline().split('"')[1]

        if email == "" or password == "":
            print(
                "Your email or password is missing. Kindly write them in credentials.txt")
            exit()

    ids = ["https://en-gb.facebook.com/" + line.split("/")[-1] for line in open(
        "C:\\ScraperFollowersAndPhotosOnly\\input.txt", newline='\n')]

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
