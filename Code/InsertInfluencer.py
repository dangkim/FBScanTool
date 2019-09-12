import json
# import requests
# response = requests.post('http://bdo8.com/connect/token', data={
#     'grant_type': 'password', 'username': 'ribisachi', 'password': '@Bcd1234', 'client_id': 'kolviet', 'client_secret': 'kolviet'
# }, headers={'Content-Type': 'application/x-www-form-urlencoded', }
# )

# json_response = response.json()
# print(json_response)

postContent = "Team nghiện bánh trung thu trứng muối chảy chảy điểm danh Năm nào Linh cũng săn lùng các loại bánh trứng muối hết, năm nay chưa gì đã falling in love với em này rùiiiii, mới lạ nhưng thơm- ngon- chảy chảy béo béo ực ực🤤🤤🤤Đi ì-zen zề đã ăn hết 4 cái rui Hại em quaaaa Nguyễn Yến ơiiiiiii sắp lăn rồiiiii"

foodKeywords = "Ăn,uống,nấu,nướng,chiên,xào,hấp,quán,xiên,luộc,bữa,dao,muỗng,nĩa,nhà hàng,khách sạn,đũa,gắp,mắm,muối,mặn,ngọt,chua,cay,gánh,bánh,cơm,nguội,khói,hổi,dĩa,tô,chén,bếp,lò,than,củi,ngon,dở,nồi,niêu,lửa,củi,hải sản,tôm,cua,cá,thịt,heo,gà,thịt bò,dai,giòn,bổ,bổ dưỡng,rau,quả,nước tương,xì dầu,mì,bưng,hủ tiếu"

listOfFoodKeyword = foodKeywords.split(",")
numberOfKey = 0
for word in listOfFoodKeyword:
    if (postContent.find(word)):
        numberOfKey = numberOfKey + 1
        if(numberOfKey > 1):
            print("food")
            break



json_string = '{"ContentItemId":"","ContentItemVersionId":"","ContentType":"Influencer","DisplayText":"","Latest":true,"Published":true,"ModifiedUtc":"","PublishedUtc":"","CreatedUtc":"","Owner":"admin","Author":"ribisachi","Influencer":{"Description":{"Text":""},"Photo":{"Paths":[],"Urls":[]},"Fanpage":{"Text":""},"Email":{"Text":""},"password":{"Text":""},"FullName":{"Text":""},"ShareLink":{"Text":""},"PostImage":{"Text":""},"LiveStream":{"Text":""},"CheckIn":{"Text":""},"Video":{"Text":""},"Phone":{"Text":""},"NumberOfLike":{"Text":""},"NumberOfComment":{"Text":""},"NumberOfLove":{"Text":""},"NumberOfShare":{"Text":""},"NumberOfReaction":{"Text":""},"VideoLink":{"Paths":[]},"NumberOfPost":{"Value":0}},"TitlePart":{"Title":""},"MyCustomPart":{"NumberOfComment":{"Text":""}},"AgeDemorgraphic":{"Percentage":{"Text":""},"AgeGraphicsName":{"Text":""},"AgePercentage":{"Text":""}},"GenderDemorgraphic":{"GenderPercentage":{"Text":""},"GenderGraphicName":{"Text":""}},"GeoDemorgraphic":{"GeoPercentage":{"Text":""},"GeoGraphicName":{"Text":""}},"Post1":{"Time":{"Text":""},"Type":{"Text":""},"Title":{"Text":""},"Status":{"Text":""},"NumberOfComment":{"Text":""},"NumberOfShare":{"Text":""},"NumberOfReaction":{"Text":""},"Link":{"Text":""}},"Post2":{"Time":{"Text":""},"Type":{"Text":""},"Title":{"Text":""},"Status":{"Text":""},"NumberOfComment":{"Text":""},"NumberOfShare":{"Text":""},"NumberOfReaction":{"Text":""},"Link":{"Text":""}},"Post3":{"Time":{"Text":""},"Type":{"Text":""},"Title":{"Text":""},"Status":{"Text":""},"NumberOfComment":{"Text":""},"NumberOfShare":{"Text":""},"NumberOfReaction":{"Text":""},"Link":{"Text":""}},"Post4":{"Time":{"Text":""},"Type":{"Text":""},"Title":{"Text":""},"Status":{"Text":""},"NumberOfComment":{"Text":""},"NumberOfShare":{"Text":""},"NumberOfReaction":{"Text":""},"Link":{"Text":""}},"Post5":{"Time":{"Text":""},"Type":{"Text":""},"Title":{"Text":""},"Status":{"Text":""},"NumberOfComment":{"Text":""},"NumberOfShare":{"Text":""},"NumberOfReaction":{"Text":""},"Link":{"Text":""}}}'

parsed_json = json.loads(json_string)
displayText = parsed_json["DisplayText"]
print(displayText)
displayText = "ribisach66"
parsed_json["DisplayText"] = displayText

print(parsed_json["DisplayText"])