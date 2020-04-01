import calendar
import os
import platform
import sys
import urllib.request
import time
import json
import requests

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# -------------------------------------------------------------
# -------------------------------------------------------------
tokenResponse = requests.post('https://bdo8.com/connect/token', verify=False, data={
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

json_string = '{"ContentItemId":"","ContentItemVersionId":"","ContentType":"Influencer","DisplayText":"","Latest":true,"Published":true,"ModifiedUtc":"","PublishedUtc":"","CreatedUtc":"","Owner":"admin","Author":"admin","Influencer":{"Description":{"Text":""},"Photo":{"Paths":[],"Urls":[]},"Fanpage":{"Text":""},"Email":{"Text":""},"password":{"Text":""},"FullName":{"Text":""},"ShareLink":{"Text":""},"PostImage":{"Text":""},"LiveStream":{"Text":""},"CheckIn":{"Text":""},"Video":{"Text":""},"Phone":{"Text":""},"NumberOfLike":{"Text":""},"NumberOfComment":{"Text":""},"NumberOfLove":{"Text":""},"NumberOfShare":{"Text":""},"NumberOfReaction":{"Text":""},"VideoLink":{"Paths":[]},"NumberOfPost":{"Value":0},"NumberOfFollowers":{"Value":0}},"TitlePart":{"Title":""},"MyCustomPart":{"NumberOfComment":{"Text":""}},"AgeDemorgraphic":{"Percentage":{"Text":""},"AgeGraphicsName":{"Text":""},"AgePercentage":{"Text":""}},"GenderDemorgraphic":{"GenderPercentage":{"Text":""},"GenderGraphicName":{"Text":""}},"GeoDemorgraphic":{"GeoPercentage":{"Text":""},"GeoGraphicName":{"Text":""}},"Post1":{"Time":{"Text":""},"Type":{"Text":""},"Title":{"Text":""},"Status":{"Text":""},"NumberOfComment":{"Text":""},"NumberOfShare":{"Text":""},"NumberOfReaction":{"Text":""},"Link":{"Text":""}},"Post2":{"Time":{"Text":""},"Type":{"Text":""},"Title":{"Text":""},"Status":{"Text":""},"NumberOfComment":{"Text":""},"NumberOfShare":{"Text":""},"NumberOfReaction":{"Text":""},"Link":{"Text":""}},"Post3":{"Time":{"Text":""},"Type":{"Text":""},"Title":{"Text":""},"Status":{"Text":""},"NumberOfComment":{"Text":""},"NumberOfShare":{"Text":""},"NumberOfReaction":{"Text":""},"Link":{"Text":""}},"Post4":{"Time":{"Text":""},"Type":{"Text":""},"Title":{"Text":""},"Status":{"Text":""},"NumberOfComment":{"Text":""},"NumberOfShare":{"Text":""},"NumberOfReaction":{"Text":""},"Link":{"Text":""}},"Post5":{"Time":{"Text":""},"Type":{"Text":""},"Title":{"Text":""},"Status":{"Text":""},"NumberOfComment":{"Text":""},"NumberOfShare":{"Text":""},"NumberOfReaction":{"Text":""},"Link":{"Text":""}}}'

foodKeywords = "Bún Bò Huế,măm măm,món ngon,nấu cơm,Ăn,uống,nấu,nướng,chiên,xào,hấp,quán,xiên,luộc,bữa,dao,muỗng,nĩa,nhà hàng,khách sạn,đũa,gắp,mắm,muối,mặn,ngọt,chua,cay,gánh,bánh,cơm,nguội,khói,hổi,dĩa,tô,chén,bếp,lò,than,củi,ngon,dở,nồi,niêu,lửa,củi,hải sản,tôm,cua,cá,thịt,heo,gà,thịt bò,dai,giòn,bổ,bổ dưỡng,rau,quả,nước tương,xì dầu,mì,bưng,hủ tiếu"
cosmeticsKeywords = "da xinh,gầy,sần sùi,hair,mái tóc,môi,son,phấn,mỹ phẩm,da,mụn,nail,móng,lông,mắt,mũi,miệng,cổ,đầu,chân,đùi,mịn,láng,nách,trắng,đen,hồng,màu,sắc,màu sắc,mông,trán,cánh tay,nhạy cảm,lông mi,lông mày,gội,xà phòng,tắm,rửa,sữa rửa,cằm,trang điểm,cá tính,đẳng cấp,kem chống nắng,chống nắng,nám,sẹo,tàn nhang,đồi mồi,body,phấn phủ,kem nền,che khuyến điểm,tẩy trang,tế bào,uốn,nhuộm,duỗi,ủ mềm,khử mùi,vệ sinh,nước hoa,mẩn ngứa,nóng rát,phù,Bong tróc,đóng vẩy,kích ứng,spa,kem"
fashionKeywords = "hair,salon,mái tóc,diện,kính,sành điệu,Miss Teen,quần,áo,giày dép,thời trang,mẫu,mẫu mã,vải,vóc,vải vóc,túi,xách,jean,lụa,tơ,mũ,nón,bóp,đầm,váy,legging,dạ hội,cưới,áo cưới,trình diễn,kiếng,kính,đồng hồ,dây kéo,nịt,lót,bikini,xa xỉ,đẳng cấp,tóc,che khuyến điểm"
sportKeywords = "gym,yoga,tập,năng động,thể thao,thể dục"
travelKeywords = "tham quan,đi chơi,chuyến đi,nắng,mưa,hè,thu,check in,xuân,đông,khách sạn,hotel,nhà nghỉ,cảnh,cảnh đẹp,hùng vĩ,thiên nhiên,ồn,ồn ào,náo nhiệt,yên tĩnh,mát,mát mẻ"
eventKeywords = "Singer,Faptv,Television,Entertainment,model,actor,Actor Comedy,giải trí,Clip,mv,video,tv,dvd,hát,event,bài hát,ca hát,đi hát,đêm nhạc,Giọng,Ca sĩ,nhạc,song,sing,ca"
housewifeKeywords = "nấu cơm,món ngon,con cái,bỉm,sữa,tã,lò,nướng,bếp,chổi,quét,gia đình,dụng cụ,nội trợ,nấu,nướng"
technologyKeywords = "down,down load,store,android,ios,phiên bản,software,phần mềm,soft,điện thoại,nhân tạo,công nghệ,kỹ thuật,app"
realestateKeywords = "nhà,đất,động sản,sổ đỏ,sổ hồng,chung cư,tầng,lầu,cầu thang,biệt thự,giấy tờ,chính chủ,quy hoạch,bản đồ,vay vốn,vốn"
furnitureKeywords = "bàn,ghế,giường,kệ tivi,tủ,salon,sofa,kệ trang,đèn,đồng hồ,gối,thảm,tranh,két sắt"
appliancesKeywords = "Nồi cơm điện,Máy Làm Mát,Điều Hòa,Lò vi sóng,Bếp ga,Bếp Âm,Bếp Từ,Hồng Ngoại,Máy hút khói,Nồi áp suất,Máy nóng lạnh,Ấm,Ca,Bình Đun,Máy lọc không khí,Máy xay sinh tố,Bình Thủy Điện,Máy ép trái cây,Máy làm sữa,Máy pha cà phê,Máy Hút Bụi,Bàn Ủi,Quạt,Máy Sấy Tóc,Đồ Dùng Nhà Bếp,Đồ dùng gia đình,Thiết Bị Chiếu Sáng,Nồi,Chảo,Máy nước nóng,Máy Lọc Nước,Bếp Nướng,Bếp gas,Bếp nướng điện,Lẩu điện,Máy đánh trứng,Máy pha cà phê,Máy hút chân không,Lò nướng,Lò vi sóng,Nồi chiên không dầu,Bình đun siêu tốc,Bình thủy điện,Máy hút mùi,Quạt,Quạt sưởi,Cây nước nóng lạnh,Bàn ủi,Máy lọc không khí,Thiết bị làm đẹp,Đèn sưởi,Máy bơm nước,bếp"
autoGameKeywords = "xe,bánh xe,siêu sang,ô tô,auto,honda,toyota,xe hơi,xe con,bốn bánh,Abarth,Alfa,Romeo,Aston,Martin,Audi,Bentley,BMW,Bugatti,Cadillac,Caterham,Chevrolet,Chrysler,Citroen,Dacia,Ferrari,Fiat,Ford,Honda,Hyundai,Infiniti,Jaguar,Jeep,Kia,Lamborghini,Rover,Lexus,Lotus,Maserati,Mazda,Mclaren,Mercedes-Benz,MG,Mini,Mitsubishi,Morgan,Nissan,Noble,Pagani,Peugeot,Porsche,Radical,Renault,Rolls-Royce,Saab,Seat,Skoda,Smart,SsangYong,Subaru,Suzuki,Tesla,Toyota,Vauxhall,Volkswagen,Volvo,Zenos,trò chơi,game,trò,down,down load,store,android,ios,phiên bản,chơi"

influencerObject = json.loads(json_string)
numberOfPost = []
wrongFaceBook = []
displayText = ""
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


def buildDisplayText(status, work):
    for word in foodKeywords.split(","):
        if ((status.find(word) != -1) or (work.find(word) != -1)):
            influencerObject["DisplayText"] += "food;"
            influencerObject["TitlePart"]["Title"] += "food;"
            break

    for word in cosmeticsKeywords.split(","):
        if ((status.find(word) != -1) or (work.find(word) != -1)):
            influencerObject["DisplayText"] += "cosmetics;"
            influencerObject["TitlePart"]["Title"] += "cosmetics;"
            break

    for word in fashionKeywords.split(","):
        if ((status.find(word) != -1) or (work.find(word) != -1)):
            influencerObject["DisplayText"] += "fashion;"
            influencerObject["TitlePart"]["Title"] += "fashion;"
            break

    for word in sportKeywords.split(","):
        if ((status.find(word) != -1) or (work.find(word) != -1)):
            influencerObject["DisplayText"] += "sport;"
            influencerObject["TitlePart"]["Title"] += "sport;"
            break

    for word in travelKeywords.split(","):
        if ((status.find(word) != -1) or (work.find(word) != -1)):
            influencerObject["DisplayText"] += "travel;"
            influencerObject["TitlePart"]["Title"] += "travel;"
            break

    for word in eventKeywords.split(","):
        if ((status.find(word) != -1) or (work.find(word) != -1)):
            influencerObject["DisplayText"] += "event;entertaining;"
            influencerObject["TitlePart"]["Title"] += "event;entertaining;"
            break

    for word in housewifeKeywords.split(","):
        if ((status.find(word) != -1) or (work.find(word) != -1)):
            influencerObject["DisplayText"] += "housewife;"
            influencerObject["TitlePart"]["Title"] += "housewife;"
            break

    for word in technologyKeywords.split(","):
        if ((status.find(word) != -1) or (work.find(word) != -1)):
            influencerObject["DisplayText"] += "app;technology;software;"
            influencerObject["TitlePart"]["Title"] += "app;technology;software;"
            break

    for word in realestateKeywords.split(","):
        if ((status.find(word) != -1) or (work.find(word) != -1)):
            influencerObject["DisplayText"] += "realestate;"
            influencerObject["TitlePart"]["Title"] += "realestate;"
            break

    for word in furnitureKeywords.split(","):
        if ((status.find(word) != -1) or (work.find(word) != -1)):
            influencerObject["DisplayText"] += "furniture;"
            influencerObject["TitlePart"]["Title"] += "furniture;"
            break

    for word in appliancesKeywords.split(","):
        if ((status.find(word) != -1) or (work.find(word) != -1)):
            influencerObject["DisplayText"] += "appliances;"
            influencerObject["TitlePart"]["Title"] += "appliances;"
            break

    for word in autoGameKeywords.split(","):
        if ((status.find(word) != -1) or (work.find(word) != -1)):
            influencerObject["DisplayText"] += "auto;game"
            influencerObject["TitlePart"]["Title"] += "auto;game"
            break


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


def get_div_links(x, tag):
    try:
        temp = x.find_element_by_xpath(".//div[@class='_3x-2']")
        return temp.find_element_by_tag_name(tag)
    except:
        return ""


def get_title_links(title):
    l = title.find_elements_by_tag_name('a')
    return l[-1].text, l[-1].get_attribute('href')


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


def extract_and_write_posts(elements, filename):
    allStatus = ""
    try:
        for x in elements:
            try:
                title = " "
                status = " "

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

                status = status.replace("\n", " ")

                allStatus += " " + status

            except:
                pass

        buildDisplayText(
            status, influencerObject["Influencer"]["Description"]["Text"])

    except:
        print("Exception (extract_and_write_posts)",
              "Status =", sys.exc_info()[0])

    return


# -------------------------------------------------------------
# -------------------------------------------------------------


def save_to_file(name, elements, status, current_section):
    """helper function used to save links to files"""
    # status 3 = dealing with about section
    # status 4 = dealing with posts

    try:
        # dealing with About Section
        if status == 3:
            workEducation = elements[0].text.replace("\n", "|")
            influencerObject["Influencer"]["Description"]["Text"] = workEducation

        # dealing with Posts
        # elif status == 4:
        #     extract_and_write_posts(elements, name)
        #     return

    except:
        print("Exception (save_to_file)", "Status =",
              str(status), sys.exc_info()[0])

    return


# ----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

def save_post(name, elements, status, current_section):
    """helper function used to save links to files"""

    try:

        # dealing with Posts
        if status == 4:
            extract_and_write_posts(elements, name)
            return

    except:
        print("Exception (save_to_file)", "Status =",
              str(status), sys.exc_info()[0])

    return


# ----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

def scrape_data_post(id, scan_list, section, elements_path, save_status, file_names):
    """Given some parameters, this function can scrap friends/photos/videos/about/posts(statuses) of a profile"""
    page = []
    folder = os.path.join(os.getcwd(), "Data")
    data = []
    if save_status == 4:
        page.append(id)

    for i in range(len(section)):
        page.append(id + section[i])

    for i in range(len(scan_list)):
        try:
            driver.get(page[i])

            if save_status != 3:
                scroll()

            data = driver.find_elements_by_xpath(elements_path[i])

            if len(data) == 0 and save_status == 4:
                data = driver.find_elements_by_xpath(
                    '//div[@class="_1dwg _1w_m _q7o"]')

            save_post(file_names[i], data, save_status, i)

        except:
            print("Exception (scrape_data)", str(i), "Status =",
                  str(save_status), sys.exc_info()[0])

    return


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

def scrape_data(id, scan_list, section, elements_path, save_status, file_names):
    """Given some parameters, this function can scrap friends/photos/videos/about/posts(statuses) of a profile"""
    page = []
    folder = os.path.join(os.getcwd(), "Data")
    data = []

    for i in range(len(section)):
        page.append(id + section[i])

    for i in range(len(scan_list)):
        try:
            driver.get(page[i])

            if save_status != 3:
                scroll()

            data = driver.find_elements_by_xpath(elements_path[i])

            if len(data) == 0 and save_status == 3:
                driver.find_element_by_class_name(
                    'see_more_link_inner').click()
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".text_exposed_root.text_exposed")))
                data = driver.find_elements_by_css_selector(
                    ".text_exposed_root.text_exposed")

            save_to_file(file_names[i], data, save_status, i)

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

# A simple function to use requests.post to make the API call. Note the json= section.


def run_query(query):

    # get influencer by userName
    tokenObject = json.loads(tokenResponse.content)
    tokenAuthorization = tokenObject['token_type'] + \
        " " + tokenObject['access_token']

    request = requests.post('https://bdo8.com/api/graphql', verify=False, json={'query': query}, headers={
        'Authorization': tokenAuthorization})

    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(
            request.status_code, query))

# --------------------------------------------------------------------------------


def scrap_profile(ids):
    folder = os.path.join(os.getcwd(), "Data")
    create_folder(folder)
    os.chdir(folder)
    # execute for all profiles given in input.txt file
    for id in ids:
        # time.sleep(4)
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

        if len(result['data']['influencer']) == 0:

            if 'Not Found' in driver.title:
                wrongFaceBook.append(id)
                continue

            try:
                expiredElement = driver.find_element_by_css_selector(
                    ".phl.ptm.uiInterstitialContent")
                if 'The link you followed may have expired' in expiredElement.text:
                    wrongFaceBook.append(id)
                    continue
            except NoSuchElementException:
                pass

            originalUrl = str(driver.current_url)
            url = originalUrl.rstrip('/')
            id = create_original_link(url)

            userName = id.rsplit('/')[-1]

            influencerObject["DisplayText"] += userName + ";"
            influencerObject["TitlePart"]["Title"] += userName + ";"

            print("\nScraping:", id)

            elements = driver.find_elements_by_xpath(
                "//*[@id='fb-timeline-cover-name']/a")

            if len(elements) == 0:
                fullNameHref = driver.find_element_by_xpath(
                    "//*[@id='seo_h1_tag']/a/span")                

                influencerObject["Influencer"]["FullName"]["Text"] = fullNameHref.text
                influencerObject["DisplayText"] += fullNameHref.text + ";"
                influencerObject["TitlePart"]["Title"] += userName + ";"

            else:
                fullNameHref = driver.find_element_by_xpath(
                    "//*[@id='fb-timeline-cover-name']/a")
                influencerObject["Influencer"]["FullName"]["Text"] = fullNameHref.text
                influencerObject["DisplayText"] += fullNameHref.text + ";"
                influencerObject["TitlePart"]["Title"] += userName + ";"

            tokenObject = json.loads(tokenResponse.content)
            tokenAuthorization = tokenObject['token_type'] + \
                " " + tokenObject['access_token']
            # insert influencer
            # influencerJson = json.dumps(influencerObject)
            influencerResponse = requests.post('https://bdo8.com/api/content/Post', verify=False, data=json.dumps(influencerObject), headers={
                'Content-Type': 'application/json', 'Authorization': tokenAuthorization})

            influencerObject["Influencer"]["FullName"]["Text"] = ""
            influencerObject["DisplayText"] = ""
            influencerObject["TitlePart"]["Title"] = ""

        print("Posts(Statuses) Done!")
        print("----------------------------------------")
    # ----------------------------------------------------------------------------

    print("Wrong Facebook:")

    for wrong in wrongFaceBook:
        print(wrong)
        pass

    print("----------------------------------------")
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
    with open('C:\\ScraperBuildKOL\\credentials.txt') as f:
        email = f.readline().split('"')[1]
        password = f.readline().split('"')[1]

        if email == "" or password == "":
            print(
                "Your email or password is missing. Kindly write them in credentials.txt")
            exit()

    ids = ["https://en-gb.facebook.com/" + line.split("/")[-1] for line in open(
        "C:\\ScraperBuildKOL\\input.txt", newline='\n')]

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
