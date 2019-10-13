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
tokenResponse = requests.post('http://dangkim:8089/connect/token', verify=False, data={
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

postModel = []

updatePostModel = {
    "posts": [],
    "contentItemId": "",
    "numberOfTotalComment": "",
    "numberOfTotalReaction": "",
    "numberOfTotalShare": "",
    "numberOfPost": ""
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

# -------------------------------------------------------------


def extract_and_write_posts(elements, filename):

    numberOfCommentTotal = 0
    numberOfReactionTotal = 0
    numberOfShareTotal = 0
    indexOfPost = 0

    try:
        for x in elements:
            try:
                indexOfPost += 1

                video_link = " "
                title = " "
                status = " "
                link = ""
                img = " "
                time = " "
                reaction = " "
                commentno = " "
                share = " "

                # share
                share = get_share(x)

                # commentno
                commentno = get_commentno(x)

                # reaction
                reaction = get_reaction(x)

                # time
                time = get_time(x)

                # title
                title = get_title(x)
                if title.text.find("shared a memory") != -1:
                    x = x.find_element_by_xpath(".//div[@class='_1dwg _1w_m']")
                    title = get_title(x)

                status = get_status(x)
                if title.text == driver.find_element_by_id("fb-timeline-cover-name").text:
                    if status == '':
                        temp = get_div_links(x, "img")
                        if temp == '':  # no image tag which means . it is not a life event
                            link = get_div_links(x, "a").get_attribute('href')
                            type = "status update without text"
                        else:
                            type = 'life event'
                            link = get_div_links(x, "a").get_attribute('href')
                            status = get_div_links(x, "a").text
                    else:
                        type = "status update"
                        if get_div_links(x, "a") != '':
                            link = get_div_links(x, "a").get_attribute('href')

                elif title.text.find(" shared ") != -1:

                    x1, link = get_title_links(title)
                    type = "shared " + x1

                elif title.text.find(" at ") != -1 or title.text.find(" in ") != -1:
                    if title.text.find(" at ") != -1:
                        x1, link = get_title_links(title)
                        type = "check in"
                    elif title.text.find(" in ") != 1:
                        status = get_div_links(x, "a").text

                elif title.text.find(" added ") != -1 and title.text.find("photo") != -1:
                    type = "added photo"
                    link = get_div_links(x, "a").get_attribute('href')

                elif title.text.find(" added ") != -1 and title.text.find("video") != -1:
                    type = "added video"
                    link = get_div_links(x, "a").get_attribute('href')

                else:
                    type = "others"

                if not isinstance(title, str):
                    title = title.text.strip()

                if not isinstance(reaction, str):
                    reaction = reaction.text

                if not isinstance(commentno, str):
                    if commentno.text.find("Comments") != -1:
                        commentno = commentno.text.replace(
                            "Comments", " ").strip()
                    elif commentno.text.find("Comment") != -1:
                        commentno = commentno.text.replace(
                            "Comment", " ").strip()

                if not isinstance(share, str):
                    if share.text.find("Shares") != -1:
                        share = share.text.replace("Shares", " ").strip()
                    elif share.text.find("Share") != -1:
                        share = share.text.replace("Share", " ").strip()

                status = status.replace("\n", " ")
                title = title.replace("\n", " ")
                reaction = reaction.replace("\n", " ")
                commentno = commentno.replace("\n", " ")
                share = share.replace("\n", " ")
                cm = getNumberFromThousand(commentno)
                rea = getNumberFromThousand(reaction)
                sh = getNumberFromThousand(share)
                numberOfCommentTotal += cm
                numberOfReactionTotal += rea
                numberOfShareTotal += sh

                postItem = {
                    "NumberOfComment": "",
                    "NumberOfReaction": "",
                    "NumberOfShare": "",
                    "Status": "",
                    "Time": "",
                    "Title": "",
                    "Type": ""
                }

                if(indexOfPost <= 5):
                    postItem['Time'] = time
                    postItem['Type'] = type
                    postItem['Title'] = title
                    postItem['Status'] = status

                    postItem['NumberOfComment'] = getThoundsandFromNumber(cm)

                    postItem['NumberOfReaction'] = getThoundsandFromNumber(rea)

                    postItem['NumberOfShare'] = getThoundsandFromNumber(sh)

                    postModel.append(postItem)

            except:
                pass

        updatePostModel['posts'] = postModel

        updatePostModel['numberOfTotalComment'] = getThoundsandFromNumber(
            numberOfCommentTotal)

        updatePostModel['numberOfTotalReaction'] = getThoundsandFromNumber(
            numberOfReactionTotal)

        updatePostModel['numberOfTotalShare'] = getThoundsandFromNumber(
            numberOfShareTotal)

        updatePostModel['numberOfPost'] = len(elements)

        # Update to database
        tokenObject = json.loads(tokenResponse.content)
        tokenAuthorization = tokenObject['token_type'] + \
            " " + tokenObject['access_token']

        updatePostModelJson = json.dumps(updatePostModel)

        influencerResponse = requests.post('https://localhost:44300/api/content/UpdatePosts', verify=False, data=updatePostModelJson, headers={
            'Content-Type': 'application/json', 'Authorization': tokenAuthorization})

    except:
        print("Exception (extract_and_write_posts)",
              "Status =", sys.exc_info()[0])

    return

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

            if (save_status == 0) or (save_status == 1) or (
                    save_status == 2):  # Only run this for friends, photos and videos

                # the bar which contains all the sections
                sections_bar = driver.find_element_by_xpath(
                    "//*[@class='_3cz'][1]/div[2]/div[1]")

                if sections_bar.text.find(scan_list[i]) == -1:
                    continue

            if save_status != 3:
                scroll()

            data = driver.find_elements_by_xpath(elements_path[i])

            save_to_file(file_names[i], data, save_status, i)

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

    try:
        # dealing with Posts
        if status == 4:
            extract_and_write_posts(elements, name)
            return
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

    request = requests.post('http://dangkim:8089/api/graphql', json={'query': query}, headers={
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
        url = driver.current_url
        id = create_original_link(url)

        userName = id.rsplit('/')[-1]

        # The GraphQL query (with a few aditional bits included) itself defined as a multi-line string.
        query = '''{{
	        influencer(where: {{displayText_contains: "{0}"}}, status: PUBLISHED) {{
                contentItemId
            }} 
        }}'''.format(userName)

        result = run_query(query)  # execute query

        updatePostModel['contentItemId'] = result['data']['influencer'][0]['contentItemId']

        print("\nScraping:", id)

        # ----------------------------------------------------------------------------
        print("----------------------------------------")
        print("Posts:")
        # setting parameters for scrape_data() to scrap posts
        scan_list = [None]
        section = []
        elements_path = ['//div[@class="_5pcb _4b0l _2q8l"]']

        file_names = ["Posts.txt"]
        save_status = 4

        scrape_data(id, scan_list, section, elements_path,
                    save_status, file_names)
        print("Posts(Statuses) Done!")
        print("----------------------------------------")

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
    with open('E:\\Kolviets\\FBScanTool\\FBScanTool\\Code\\credentials.txt') as f:
        email = f.readline().split('"')[1]
        password = f.readline().split('"')[1]

        if email == "" or password == "":
            print(
                "Your email or password is missing. Kindly write them in credentials.txt")
            exit()

    ids = ["https://en-gb.facebook.com/" + line.split("/")[-1] for line in open(
        "E:\\Kolviets\\FBScanTool\\FBScanTool\\Code\\input.txt", newline='\n')]

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
