import os
import platform
import sys
import urllib.request
import json
import time as t
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import utils
import postUtils

# -------------------------------------------------------------
# -------------------------------------------------------------


# Global Variables

driver = None

# whether to download photos or not
download_uploaded_photos = True
download_friends_photos = True

# whether to download the full image or its thumbnail (small size)
# if small size is True then it will be very quick else if its false then it will open each photo to download it
# and it will take much more time
friends_small_size = True
photos_small_size = False

total_scrolls = 5
current_scrolls = 10
scroll_time = 5

old_height = 0

json_string = '{"ContentItemId":"","ContentItemVersionId":"","ContentType":"Influencer","DisplayText":"","Latest":true,"Published":true,"ModifiedUtc":"","PublishedUtc":"","CreatedUtc":"","Owner":"admin","Author":"ribisachi","Influencer":{"Description":{"Text":""},"Photo":{"Paths":[],"Urls":[]},"Fanpage":{"Text":""},"Email":{"Text":""},"password":{"Text":""},"FullName":{"Text":""},"ShareLink":{"Text":""},"PostImage":{"Text":""},"LiveStream":{"Text":""},"CheckIn":{"Text":""},"Video":{"Text":""},"Phone":{"Text":""},"NumberOfLike":{"Text":""},"NumberOfComment":{"Text":""},"NumberOfLove":{"Text":""},"NumberOfShare":{"Text":""},"NumberOfReaction":{"Text":""},"VideoLink":{"Paths":[]},"NumberOfPost":{"Value":0},"NumberOfFollowers":{"Value":0}},"TitlePart":{"Title":""},"MyCustomPart":{"NumberOfComment":{"Text":""}},"AgeDemorgraphic":{"Percentage":{"Text":""},"AgeGraphicsName":{"Text":""},"AgePercentage":{"Text":""}},"GenderDemorgraphic":{"GenderPercentage":{"Text":""},"GenderGraphicName":{"Text":""}},"GeoDemorgraphic":{"GeoPercentage":{"Text":""},"GeoGraphicName":{"Text":""}},"Post1":{"Time":{"Text":""},"Type":{"Text":""},"Title":{"Text":""},"Status":{"Text":""},"NumberOfComment":{"Text":""},"NumberOfShare":{"Text":""},"NumberOfReaction":{"Text":""},"Link":{"Text":""}},"Post2":{"Time":{"Text":""},"Type":{"Text":""},"Title":{"Text":""},"Status":{"Text":""},"NumberOfComment":{"Text":""},"NumberOfShare":{"Text":""},"NumberOfReaction":{"Text":""},"Link":{"Text":""}},"Post3":{"Time":{"Text":""},"Type":{"Text":""},"Title":{"Text":""},"Status":{"Text":""},"NumberOfComment":{"Text":""},"NumberOfShare":{"Text":""},"NumberOfReaction":{"Text":""},"Link":{"Text":""}},"Post4":{"Time":{"Text":""},"Type":{"Text":""},"Title":{"Text":""},"Status":{"Text":""},"NumberOfComment":{"Text":""},"NumberOfShare":{"Text":""},"NumberOfReaction":{"Text":""},"Link":{"Text":""}},"Post5":{"Time":{"Text":""},"Type":{"Text":""},"Title":{"Text":""},"Status":{"Text":""},"NumberOfComment":{"Text":""},"NumberOfShare":{"Text":""},"NumberOfReaction":{"Text":""},"Link":{"Text":""}}}'

influencerObject = json.loads(json_string)
numberOfPost = []
displayText = ""


# -------------------------------------------------------------
# -------------------------------------------------------------

def get_facebook_images_url(img_links):
    urls = []

    for link in img_links:
        if link != "None":
            valid_url_found = False
            driver.get(link)
            try:
                while not valid_url_found:
                    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//img")))
                    img_url = driver.find_elements(By.XPATH, "//img")[0].get_attribute('src')
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
# -------------------------------------------------------------

# takes a url and downloads image from that url
def image_downloader(img_links, folder_name, username=''):
    img_names = []

    try:
        parent = os.getcwd()
        try:
            folder = os.path.join(os.getcwd(), folder_name)
            create_folder(folder)
            os.chdir(folder)
        except:
            print("Error in changing directory.")
        # index = 0
        for link in img_links:
            # index = index + 1
            img_name = "None"
            if link != "None":
                img_name = (link.split('.jpg')[0]).split('/')[-1] + '.jpg'
                # img_name = username + '.jpg'
                # this is the image id when there's no profile pic
                if img_name == "10354686_10150004552801856_220367501106153455_n.jpg":
                    img_name = "None"
                else:
                    try:
                        urllib.request.urlretrieve(link, img_name)
                    except:
                        img_name = "None"
            img_names.append(img_name)
        os.chdir(parent)
    except:
        print("Exception (image_downloader):", sys.exc_info()[0])

    return img_names


# -------------------------------------------------------------
# -------------------------------------------------------------

def check_height():
    new_height = driver.execute_script("return document.body.scrollHeight")
    return new_height != old_height


# -------------------------------------------------------------
# -------------------------------------------------------------

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


# -------------------------------------------------------------
# -------------------------------------------------------------

# --Helper Functions for Posts


def get_div_links(x, tag):
    try:
        temp = x.find_element_by_xpath(".//div[@class='_3x-2']")
        return temp.find_element_by_tag_name(tag)
    except NoSuchElementException:
        return ""


def get_title_links(title):
    l = title.find_elements_by_tag_name('a')
    return l[-1].text, l[-1].get_attribute('href')



def extract_and_write_posts(elements, filename):
    try:
        f = open(filename, 'w', encoding='utf-8', newline='\r\n')
        f.writelines(
            ' TIME | TYPE  | TITLE | STATUS | REACTIVE | COMMENTNO | SHARE |LINKS(Shared Posts/Shared Links etc) ' + '\n' + '\n')
        driver.execute_script("window.scrollTo(document.body.scrollHeight, 0)")
        t.sleep(3)
        for x in elements:
            try:
                video_link = " "
                title = " "
                status = " "
                link = ""
                img = " "
                time = " "
                reactive = " "
                commentno = " "
                share = " "
                # Number of Comments
                commentno = postUtils.get_comment_number(x)
                # share
                share = postUtils.get_share(x)
                # reactive
                reactive = postUtils.get_reactive(x)
                # time
                # TODO
                time = postUtils.get_time(x)
                # title
                title = postUtils.get_title(x)
                # TODO
                # status = postUtils.get_status(x)
                # if title.text == driver.find_element_by_id("fb-timeline-cover-name").text:
                #     if status == '':
                #         temp = get_div_links(x, "img")
                #         if temp == '':  # no image tag which means . it is not a life event
                #             link = get_div_links(x, "a").get_attribute('href')
                #             type = "status update without text"
                #         else:
                #             type = 'life event'
                #             link = get_div_links(x, "a").get_attribute('href')
                #             status = get_div_links(x, "a").text
                #     else:
                #         type = "status update"
                #         if get_div_links(x, "a") != '':
                #             link = get_div_links(x, "a").get_attribute('href')
                #
                # elif title.text.find(" shared ") != -1:
                #
                #     x1, link = get_title_links(title)
                #     type = "shared " + x1
                #
                # elif title.text.find(" at ") != -1 or title.text.find(" in ") != -1:
                #     if title.text.find(" at ") != -1:
                #         x1, link = get_title_links(title)
                #         type = "check in"
                #     elif title.text.find(" in ") != 1:
                #         status = get_div_links(x, "a").text
                #
                # elif title.text.find(" added ") != -1 and title.text.find("photo") != -1:
                #     type = "added photo"
                #     link = get_div_links(x, "a").get_attribute('href')
                #
                # elif title.text.find(" added ") != -1 and title.text.find("video") != -1:
                #     type = "added video"
                #     link = get_div_links(x, "a").get_attribute('href')
                #
                # else:
                #     type = "others"

                status = status.replace("\n", " ")
                title = title.replace("\n", " ")
                reactive = reactive.replace("\n", " ")
                commentno = commentno.replace("\n", " ")
                share = share.replace("\n", " ")

                line = str(time) + " | " + str(type) + ' | ' + str(title) + ' | ' + str(status) + ' | ' + str(
                    reactive) + ' | ' + str(commentno) + ' | ' + str(share) + ' | ' + str(link) + "\n"

                try:
                    f.writelines(line)
                except NoSuchElementException:
                    print('Posts: Could not map encoded characters')
            except NoSuchElementException:
                pass
        f.close()
    except NoSuchElementException:
        print("Exception (extract_and_write_posts)",
              "Status =", sys.exc_info()[0])

    return


# -------------------------------------------------------------
# -------------------------------------------------------------


def save_to_file(name, elements, status, current_section, username=''):
    """helper function used to save links to files"""

    # status 0 = dealing with friends list
    # status 1 = dealing with photos
    # status 2 = dealing with videos
    # status 3 = dealing with about section
    # status 4 = dealing with posts

    try:
        f = None  # file pointer

        if status != 4:
            f = open(name, 'w', encoding='utf-8', newline='\r\n')

        results = []
        img_names = []

        # dealing with Friends
        if status == 0:
            # get profile links of friends
            results = []
            people_names = []
            for element in elements:
                try:
                    links_of_friends = element.find_element_by_xpath('./div[2]/div[1]/a').get_attribute('href')
                    if 'pages' not in links_of_friends:
                        results.append(links_of_friends)
                        # get names of friends
                        if element.text.split('\n')[0]:
                            people_names.append(element.text.split('\n')[0])

                except NoSuchElementException:
                    continue
            results = [utils.create_original_link(x) for x in results]

            # download friends' photos
            try:
                if download_friends_photos:
                    if friends_small_size:
                        # img_links = [x.find_element_by_css_selector(
                        #     'img').get_attribute('src') for x in elements]
                        img_links = []
                        for element in elements:
                            try:
                                img_links.append(element.find_element_by_xpath('./div[1]/a/img').get_attribute('src'))

                            except NoSuchElementException:
                                continue
                    else:
                        links = []
                        for friend in results:
                            try:
                                driver.get(friend)
                                WebDriverWait(driver, 30).until(
                                    EC.presence_of_element_located((By.CLASS_NAME, "profilePicThumb")))
                                l = driver.find_element_by_class_name(
                                    "profilePicThumb").get_attribute('href')
                            except:
                                l = "None"

                            links.append(l)

                        for i in range(len(links)):
                            if links[i] is None:
                                links[i] = "None"
                            elif links[i].find('picture/view') != -1:
                                links[i] = "None"

                        img_links = get_facebook_images_url(links)

                    folder_names = ["Friend's Photos", "Mutual Friends' Photos", "Following's Photos",
                                    "Follower's Photos", "Work Friends Photos",
                                    "College Friends Photos", "Current City Friends Photos", "Hometown Friends Photos"]
                    print("Downloading " + folder_names[current_section])

                    img_names = image_downloader(
                        img_links, folder_names[current_section], username)
                else:
                    img_names = ["None"] * len(results)
            except:
                print("Exception (Images)", str(status), "Status =",
                      current_section, sys.exc_info()[0])

        # dealing with Photos
        # Influencer Photos
        elif status == 1:
            results = [x.get_attribute('src') for x in elements]
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
                    print("Downloading " + folder_names[current_section])

                    img_names = image_downloader(
                        background_img_links, folder_names[current_section], username)

                else:
                    img_names = ["None"] * len(results)
            except:
                print("Exception (Images)", str(status), "Status =",
                      current_section, sys.exc_info()[0])

        # dealing with Videos
        elif status == 2:
            results = [x.get_attribute('src') for x in elements]
        # dealing with About Section
        elif status == 3:
            if elements:
                results = elements[0].text
                f.writelines(results)

        # dealing with Posts
        elif status == 4:
            extract_and_write_posts(elements, name)
            return

        """Write results to file"""
        if status == 0:
            for i in range(len(results)):
                # friend's profile link
                f.writelines(results[i])
                f.write(',')

                # friend's name
                f.writelines(people_names[i])
                f.write(',')

                # friend's downloaded picture id
                f.writelines(img_names[i])
                f.write('\n')

        elif status == 1:
            print(results)
            for i in range(len(results)):
                # image's link
                f.writelines(results[i])
                f.write(',')

                # downloaded picture id
                f.writelines(img_names[i])
                f.write('\n')

        elif status == 2:
            for x in results:
                f.writelines(x + "\n")

        f.close()

    except:
        print("Exception (save_to_file)", "Status =",
              str(status), sys.exc_info()[0])

    return


# ----------------------------------------------------------------------------
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
                sections_bar = driver.find_elements(By.XPATH,
                                                    "//div[@class='x6s0dn4 x9f619 x2lah0s x1hshjfz x1n2onr6 x3nfvp2 xrbpyxo x16dsc37 xng8ra x1pi30zi x1swvt13']")
                is_in_correct_section = False
                for section in sections_bar:
                    section_text = section.find_element_by_xpath('./*').get_attribute("innerHTML")
                    if scan_list[i] in section_text:
                        is_in_correct_section = True
                        break
                if not is_in_correct_section:
                    continue

            if save_status != 3:
                scroll()

            # data = driver.find_elements_by_xpath(elements_path[i])
            if save_status == 4:
                t.sleep(3)

            data = driver.find_elements(By.XPATH, elements_path[i])
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


def scrap_profile(ids):
    folder = os.path.join(os.getcwd(), "Data")
    create_folder(folder)
    os.chdir(folder)
    # Execute for all profiles given in input.txt file
    for id in ids:
        driver.get(id)
        url = driver.current_url
        id = utils.create_original_link(url)
        print("\nScraping:", id)
        try:
            follower_span = driver.find_element_by_xpath('//a[@href="' + id + "/followers" + '"]')
            influencerObject["Influencer"]["NumberOfFollowers"]["Value"] = follower_span.text.replace(' people',
                                                                                                      '').replace(',',
                                                                                                                  '',
                                                                                                                  100)
        except NoSuchElementException:
            pass
        try:
            target_dir = utils.get_profile_folder(folder, id)
            create_folder(target_dir)
            os.chdir(target_dir)
        except:
            print("Some error occurred in creating the profile directory.")
            continue

        # ----------------------------------------------------------------------------
        print("----------------------------------------")
        print("Friends..")
        # setting parameters for scrape_data() to scrape friends
        scan_list = ["All friends",
                     "Mutual friends",
                     "Following",
                     "Followers",
                     "Work",
                     "University",
                     "Current City",
                     "Home Town"]
        section = utils.get_friend_section_route(url)
        elements_path = ["//div[@class='x6s0dn4 x1lq5wgf xgqcy7u x30kzoy x9jhf4c x1olyfxc x9f619 x78zum5 x1e56ztr xyamay9 x1pi30zi x1l90r2v x1swvt13 x1gefphp']"] * 8
        file_names = ["All Friends.txt",
                      "Mutual Friends.txt",
                      "Following.txt",
                      "Followers.txt",
                      "Work Friends.txt",
                      "College Friends.txt",
                      "Current City Friends.txt",
                      "Hometown Friends.txt"]
        save_status = 0
        scrape_data(id, scan_list, section, elements_path, save_status, file_names)
        print("Friends Done!")

        # ----------------------------------------------------------------------------

        print("----------------------------------------")
        print("Photos..")
        print("Scraping Links..")
        # setting parameters for scrape_data() to scrap photos
        scan_list = ["'s Photos", "Photos of"]
        section = utils.get_photos_section_route(url)
        elements_path = ["//img[@class='xzg4506 xycxndf xua58t2 x4xrfw5 x1lq5wgf xgqcy7u x30kzoy x9jhf4c x9f619 x5yr21d xl1xv1r xh8yej3']"] * 2
        file_names = ["Uploaded Photos.txt", "Tagged Photos.txt"]
        save_status = 1

        scrape_data(id, scan_list, section, elements_path, save_status, file_names)
        print("Photos Done!")

        # ----------------------------------------------------------------------------
        print("----------------------------------------")
        print("Videos:")
        # setting parameters for scrape_data() to scrap videos
        scan_list = ["'s Videos", "Videos of"]
        section = utils.get_video_section_route(url)
        elements_path = ["//img[@class='xzg4506 xycxndf xua58t2 x4xrfw5 x1lq5wgf xgqcy7u x30kzoy x9jhf4c x9f619 x5yr21d xl1xv1r xh8yej3']"] * 2
        file_names = ["Uploaded Videos.txt", "Tagged Videos.txt"]
        save_status = 2

        scrape_data(id, scan_list, section, elements_path, save_status, file_names)
        print("Videos Done!")
        # ----------------------------------------------------------------------------

        print("----------------------------------------")
        print("About:")
        # setting parameters for scrape_data() to scrap the about section
        scan_list = [None] * 7
        section = utils.get_about_section_route(url)
        elements_path = ["//div[@class='x9f619 x1n2onr6 x1ja2u2z x78zum5 x2lah0s x1nhvcw1 x1qjc9v5 xozqiw3 x1q0g3np xexx8yu xykv574 xbmpl8g x4cne27 xifccgj']/div[2]/div[1]/span"] * 7
        file_names = ["Overview.txt",
                      "Work and Education.txt",
                      "Places Lived.txt",
                      "Contact and Basic Info.txt",
                      "Family and Relationships.txt",
                      "Details About.txt",
                      "Life Events.txt"]
        save_status = 3

        scrape_data(id, scan_list, section, elements_path, save_status, file_names)
        print("About Section Done!")

        # ----------------------------------------------------------------------------
        print("----------------------------------------")
        print("Posts:")
        # setting parameters for scrape_data() to scrap posts
        scan_list = [None]
        section = []
        elements_path = ['//div[@class="x1ja2u2z xh8yej3 x1n2onr6 x1yztbdb"]']

        file_names = ["Posts.txt"]
        save_status = 4

        scrape_data(id, scan_list, section, elements_path,
                    save_status, file_names)
        print("Posts(Statuses) Done!")
        print("----------------------------------------")
    # ----------------------------------------------------------------------------

    print("\nProcess Completed.")

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
                options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
                driver = webdriver.Chrome(
                    executable_path="F:\\Project\\KOLS\\KOLS\\Code\\chromedriver.exe", options=options)
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
        driver.find_element_by_name('login').click()

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
    with open('F:\\Project\\KOLS\\KOLS\\Code\\credentials.txt') as f:
        email = f.readline().split('"')[1]
        password = f.readline().split('"')[1]

        if email == "" or password == "":
            print(
                "Your email or password is missing. Kindly write them in credentials.txt")
            exit()

    ids = ["https://en-gb.facebook.com/" + line.split("/")[-1] for line in open(
        "F:\\Project\\KOLS\\KOLS\\Code\\input1.txt", newline='\n')]

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
