import calendar
import os
import platform
import sys
import urllib.request
import time
import json

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# -------------------------------------------------------------
# -------------------------------------------------------------


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

foodKeywords = "Ăn,uống,nấu,nướng,chiên,xào,hấp,quán,xiên,luộc,bữa,dao,muỗng,nĩa,nhà hàng,khách sạn,đũa,gắp,mắm,muối,mặn,ngọt,chua,cay,gánh,bánh,cơm,nguội,khói,hổi,dĩa,tô,chén,bếp,lò,than,củi,ngon,dở,nồi,niêu,lửa,củi,hải sản,tôm,cua,cá,thịt,heo,gà,thịt bò,dai,giòn,bổ,bổ dưỡng,rau,quả,nước tương,xì dầu,mì,bưng,hủ tiếu"
cosmeticsKeywords = "môi,son,phấn,mỹ phẩm,da,mụn,nail,móng,lông,mắt,mũi,miệng,cổ,đầu,chân,đùi,mịn,láng,nách,trắng,đen,hồng,màu,sắc,màu sắc,mông,trán,cánh tay,nhạy cảm,lông mi,lông mày,gội,xà phòng,tắm,rửa,sữa rửa,cằm,trang điểm,cá tính,đẳng cấp,kem chống nắng,chống nắng,nám,sẹo,tàn nhang,đồi mồi,body,phấn phủ,kem nền,che khuyến điểm,tẩy trang,tế bào,uốn,nhuộm,duỗi,ủ mềm,khử mùi,vệ sinh,nước hoa,mẩn ngứa,nóng rát,phù,Bong tróc,đóng vẩy,kích ứng,spa,kem"
fashionKeywords = "quần,áo,giày dép,thời trang,mẫu,mẫu mã,vải,vóc,vải vóc,túi,xách,jean,lụa,tơ,mũ,nón,bóp,đầm,váy,legging,dạ hội,cưới,áo cưới,trình diễn,kiếng,kính,đồng hồ,dây kéo,nịt,lót,bikini,xa xỉ,đẳng cấp,tóc,che khuyến điểm"
sportKeywords = "gym,yoga,tập,năng động,thể thao,thể dục"
travelKeywords = "nắng,mưa,hè,thu,check in,xuân,đông,khách sạn,hotel,nhà nghỉ,cảnh,cảnh đẹp,hùng vĩ,thiên nhiên,ồn,ồn ào,náo nhiệt,yên tĩnh,mát,mát mẻ"
eventKeywords = "giải trí,Clip,mv,video,tv,dvd,hát,event,bài hát,ca hát,đi hát,đêm nhạc,Giọng,Ca sĩ,nhạc,song,sing,ca"
housewifeKeywords = "con,con cái,bỉm,sữa,tã,núc,lò,nướng,bếp,nhà,cửa,chổi,quét,gia đình,dụng cụ,nội trợ,nấu,nướng"
technologyKeywords = "down,down load,store,android,ios,phiên bản,software,phần mềm,soft,điện thoại,nhân tạo,công nghệ,kỹ thuật,app"
realestateKeywords = "nhà,đất,động sản,sổ đỏ,sổ hồng,chung cư,tầng,lầu,cầu thang,biệt thự,giấy tờ,chính chủ,quy hoạch,bản đồ,vay vốn,vốn"
furnitureKeywords = "bàn,ghế,giường,kệ tivi,tủ,salon,sofa,kệ trang,đèn,đồng hồ,gối,thảm,tranh,két sắt"
appliancesKeywords = "Nồi cơm điện,Máy Làm Mát,Điều Hòa,Lò vi sóng,Bếp ga,Bếp Âm,Bếp Từ,Hồng Ngoại,Máy hút khói,Nồi áp suất,Máy nóng lạnh,Ấm,Ca,Bình Đun,Máy lọc không khí,Máy xay sinh tố,Bình Thủy Điện,Máy ép trái cây,Máy làm sữa,Máy pha cà phê,Máy Hút Bụi,Bàn Ủi,Quạt,Máy Sấy Tóc,Đồ Dùng Nhà Bếp,Đồ dùng gia đình,Thiết Bị Chiếu Sáng,Nồi,Chảo,Máy nước nóng,Máy Lọc Nước,Bếp Nướng,Bếp gas,Bếp nướng điện,Lẩu điện,Máy đánh trứng,Máy pha cà phê,Máy hút chân không,Lò nướng,Lò vi sóng,Nồi chiên không dầu,Bình đun siêu tốc,Bình thủy điện,Máy hút mùi,Quạt,Quạt sưởi,Cây nước nóng lạnh,Bàn ủi,Máy lọc không khí,Thiết bị làm đẹp,Đèn sưởi,Máy bơm nước,bếp"
autoGameKeywords = "xe,bánh xe,siêu sang,ô tô,auto,honda,toyota,xe hơi,xe con,bốn bánh,Abarth,Alfa,Romeo,Aston,Martin,Audi,Bentley,BMW,Bugatti,Cadillac,Caterham,Chevrolet,Chrysler,Citroen,Dacia,Ferrari,Fiat,Ford,Honda,Hyundai,Infiniti,Jaguar,Jeep,Kia,Lamborghini,Rover,Lexus,Lotus,Maserati,Mazda,Mclaren,Mercedes-Benz,MG,Mini,Mitsubishi,Morgan,Nissan,Noble,Pagani,Peugeot,Porsche,Radical,Renault,Rolls-Royce,Saab,Seat,Skoda,Smart,SsangYong,Subaru,Suzuki,Tesla,Toyota,Vauxhall,Volkswagen,Volvo,Zenos,trò chơi,game,trò,down,down load,store,android,ios,phiên bản,chơi"

influencerObject = json.loads(json_string)
numberOfPost = []
displayText = ""
workEducation = ""
# -------------------------------------------------------------
# -------------------------------------------------------------


def get_facebook_images_url(img_links):
    urls = []
    index = 0
    for link in img_links:
        index += 1
        if index > 2:
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
# -------------------------------------------------------------

# takes a url and downloads image from that url
def image_downloader(img_links, folder_name, username=''):
    img_names = []
    photoLinks = []
    try:
        parent = os.getcwd()
        try:
            folder = os.path.join(os.getcwd(), folder_name)
            create_folder(folder)
            os.chdir(folder)
        except:
            print("Error in changing directory.")

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

        influencerObject["Influencer"]["Photo"]["Paths"] = photoLinks

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

def buildDisplayText(status, work):
    # resourse = []
    # resourse.append(foodKeywords.split(","))
    # resourse.append(cosmeticsKeywords.split(","))
    # resourse.append(fashionKeywords.split(","))
    # resourse.append(sportKeywords.split(","))
    # resourse.append(travelKeywords.split(","))
    # resourse.append(eventKeywords.split(","))
    # resourse.append(housewifeKeywords.split(","))
    # resourse.append(technologyKeywords.split(","))
    # resourse.append(realestateKeywords.split(","))
    # resourse.append(furnitureKeywords.split(","))
    # resourse.append(appliancesKeywords.split(","))
    # resourse.append(autoGameKeywords.split(","))

    for word in foodKeywords.split(","):
        if ((status.find(word) != -1) or (work.find(word) != -1)):
            influencerObject["DisplayText"] += "food;"
            break

    for word in cosmeticsKeywords.split(","):
        if ((status.find(word) != -1) or (work.find(word) != -1)):
            influencerObject["DisplayText"] += "cosmetics;"
            break

    for word in fashionKeywords.split(","):
        if ((status.find(word) != -1) or (work.find(word) != -1)):
            influencerObject["DisplayText"] += "fashion;"
            break

    for word in sportKeywords.split(","):
        if ((status.find(word) != -1) or (work.find(word) != -1)):
            influencerObject["DisplayText"] += "sport;"
            break

    for word in travelKeywords.split(","):
        if ((status.find(word) != -1) or (work.find(word) != -1)):
            influencerObject["DisplayText"] += "travel;"
            break

    for word in eventKeywords.split(","):
        if ((status.find(word) != -1) or (work.find(word) != -1)):
            influencerObject["DisplayText"] += "event;entertaining;"
            break

    for word in housewifeKeywords.split(","):
        if ((status.find(word) != -1) or (work.find(word) != -1)):
            influencerObject["DisplayText"] += "housewife;"
            break

    for word in technologyKeywords.split(","):
        if ((status.find(word) != -1) or (work.find(word) != -1)):
            influencerObject["DisplayText"] += "app;technology;software;"
            break

    for word in realestateKeywords.split(","):
        if ((status.find(word) != -1) or (work.find(word) != -1)):
            influencerObject["DisplayText"] += "realestate;"
            break

    for word in furnitureKeywords.split(","):
        if ((status.find(word) != -1) or (work.find(word) != -1)):
            influencerObject["DisplayText"] += "furniture;"
            break

    for word in appliancesKeywords.split(","):
        if ((status.find(word) != -1) or (work.find(word) != -1)):
            influencerObject["DisplayText"] += "appliances;"
            break

    for word in autoGameKeywords.split(","):
        if ((status.find(word) != -1) or (work.find(word) != -1)):
            influencerObject["DisplayText"] += "auto;game"
            break


def getNumberFromThousand(x):
    if not x:
        return 0
    numberOfValue = x.rsplit('k', 1)
    if len(numberOfValue) > 1:
        return float(numberOfValue[0] * 1000)
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


def extract_and_write_posts(elements, filename):

    numberOfCommentTotal = 0
    numberOfReactionTotal = 0
    numberOfShareTotal = 0
    indexOfPost = 0

    try:
        f = open(filename, 'w', encoding='utf-8', newline='\r\n')
        f.writelines(
            ' TIME | TYPE  | TITLE | STATUS | REACTIVE | COMMENTNO | SHARE |LINKS(Shared Posts/Shared Links etc) ' + '\n' + '\n')

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

                if(indexOfPost <= 5):
                    influencerObject["Post" +
                                     str(indexOfPost)]["Time"]["Text"] = time
                    influencerObject["Post" +
                                     str(indexOfPost)]["Type"]["Text"] = type
                    influencerObject["Post" +
                                     str(indexOfPost)]["Title"]["Text"] = title
                    influencerObject["Post" +
                                     str(indexOfPost)]["Status"]["Text"] = status

                    influencerObject["Post" +
                                     str(indexOfPost)]["NumberOfComment"]["Text"] = cm

                    influencerObject["Post" +
                                     str(indexOfPost)]["NumberOfReaction"]["Text"] = rea
                                     
                    influencerObject["Post" +
                                     str(indexOfPost)]["NumberOfShare"]["Text"] = sh

                line = str(time) + " | " + str(type) + ' | ' + str(title) + ' | ' + str(status) + ' | ' + str(reaction) + ' | ' + str(commentno) + ' | ' + str(share) + ' | ' + str(
                    link) + "\n"

                try:
                    f.writelines(line)
                except:
                    print('Posts: Could not map encoded characters')
            except:
                pass

        influencerObject["Influencer"]["NumberOfComment"]["Text"] = getThoundsandFromNumber(
            numberOfCommentTotal)
        influencerObject["Influencer"]["NumberOfReaction"]["Text"] = getThoundsandFromNumber(
            numberOfReactionTotal)
        influencerObject["Influencer"]["NumberOfShare"]["Text"] = getThoundsandFromNumber(
            numberOfShareTotal)
        influencerObject["Influencer"]["NumberOfPost"]["Value"] = len(elements)

        buildDisplayText(status, workEducation)

        f.close()
    except:
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
        videoLinks = []

        # dealing with Photos
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

        # dealing with About Section
        elif status == 3:
            workEducation = elements[0].text
            influencerObject["Influencer"]["Description"]["Text"] = workEducation
            f.writelines(workEducation)

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
                videoLinks.append(x)
                f.writelines(x + "\n")
            influencerObject["Influencer"]["VideoLink"]["Paths"] = videoLinks
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
                sections_bar = driver.find_element_by_xpath(
                    "//*[@class='_3cz'][1]/div[2]/div[1]")

                if sections_bar.text.find(scan_list[i]) == -1:
                    continue

            if save_status != 3:
                scroll()

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


def scrap_profile(ids):
    folder = os.path.join(os.getcwd(), "Data")
    create_folder(folder)
    os.chdir(folder)

    # execute for all profiles given in input.txt file
    for id in ids:

        driver.get(id)
        url = driver.current_url
        id = create_original_link(url)

        print("\nScraping:", id)

        followerSpan = driver.find_element_by_xpath(
            "//*[@id='profileEscapeHatchContentID']/div[2]/div/div[2]/div[2]/div[2]/span")
        influencerObject["Influencer"]["NumberOfFollowers"]["Value"] = followerSpan.text

        fullNameHref = driver.find_element_by_xpath(
            "//*[@id='fb-timeline-cover-name']/a")
        influencerObject["Influencer"]["FullName"]["Text"] = fullNameHref.text

        try:
            target_dir = os.path.join(folder, id.split('/')[-1])
            create_folder(target_dir)
            os.chdir(target_dir)
        except:
            print("Some error occurred in creating the profile directory.")
            continue

        print("----------------------------------------")
        print("Photos..")
        print("Scraping Links..")
        # setting parameters for scrape_data() to scrap photos
        scan_list = ["'s Photos", "Photos of"]
        section = ["/photos_all", "/photos_of"]
        elements_path = ["//*[contains(@id, 'pic_')]"] * 2
        file_names = ["Uploaded Photos.txt", "Tagged Photos.txt"]
        save_status = 1

        scrape_data(id, scan_list, section, elements_path,
                    save_status, file_names)
        print("Photos Done!")

        # ----------------------------------------------------------------------------
        print("----------------------------------------")
        print("Videos:")
        # setting parameters for scrape_data() to scrap videos
        scan_list = ["'s Videos", "Videos of"]
        section = ["/videos_by", "/videos_of"]
        elements_path = [
            "//*[contains(@id, 'pagelet_timeline_app_collection_')]/ul"] * 2
        file_names = ["Uploaded Videos.txt", "Tagged Videos.txt"]
        save_status = 2

        scrape_data(id, scan_list, section, elements_path,
                    save_status, file_names)
        print("Videos Done!")
        # ----------------------------------------------------------------------------

        print("----------------------------------------")
        print("About:")
        # setting parameters for scrape_data() to scrap the about section
        scan_list = [None] * 1
        section = ["/about?section=education"]
        elements_path = [
            "//*[contains(@id, 'pagelet_timeline_app_collection_')]/ul/li/div/div[2]/div/div"] * 7
        file_names = ["Work and Education.txt"]
        save_status = 3

        scrape_data(id, scan_list, section, elements_path,
                    save_status, file_names)
        print("About Section Done!")

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
    with open('D:\\workspace\\Ultimate-Facebook-Scraper\\Code\\credentials.txt') as f:
        email = f.readline().split('"')[1]
        password = f.readline().split('"')[1]

        if email == "" or password == "":
            print(
                "Your email or password is missing. Kindly write them in credentials.txt")
            exit()

    ids = ["https://en-gb.facebook.com/" + line.split("/")[-1] for line in open(
        "D:\\workspace\\Ultimate-Facebook-Scraper\\Code\\input.txt", newline='\n')]

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
