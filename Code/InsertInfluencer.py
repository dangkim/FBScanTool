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
cosmeticsKeywords = "son,phấn,mỹ phẩm,da,mụn,nail,móng,lông,mắt,mũi,miệng,cổ,đầu,chân,đùi,mịn,láng,nách,trắng,đen,hồng,màu,sắc,màu sắc,mông,trán,cánh tay,nhạy cảm,lông mi,lông mày,gội,xà phòng,tắm,rửa,sữa rửa,cằm,trang điểm,cá tính,đẳng cấp,kem chống nắng,chống nắng,nám,sẹo,tàn nhang,đồi mồi,body,phấn phủ,kem nền,che khuyến điểm,tẩy trang,tế bào,uốn,nhuộm,duỗi,ủ mềm,khử mùi,vệ sinh,nước hoa,mẩn ngứa,nóng rát,phù,Bong tróc,đóng vẩy,kích ứng,spa,kem"
fashionKeywords = "quần,áo,giày dép,thời trang,mẫu,mẫu mã,vải,vóc,vải vóc,túi,xách,jean,lụa,tơ,mũ,nón,bóp,đầm,váy,legging,dạ hội,cưới,áo cưới,trình diễn,kiếng,kính,đồng hồ,dây kéo,nịt,lót,bikini,xa xỉ,đẳng cấp,tóc,che khuyến điểm"
sportKeywords = "gym,yoga,tập,năng động,thể thao,thể dục"
travelKeywords = "nắng,mưa,hè,thu,check in,xuân,đông,khách sạn,hotel,nhà nghỉ,cảnh,cảnh đẹp,hùng vĩ,thiên nhiên,ồn,ồn ào,náo nhiệt,yên tĩnh,mát,mát mẻ"
eventKeywords = "Clip,mv,video,tv,dvd,hát,event,bài hát,ca hát,đi hát,đêm nhạc,song,sing"
housewifeKeywords = "con,con cái,bỉm,sữa,tã,núc,lò,nướng,bếp,nhà,cửa,chổi,quét,gia đình,dụng cụ,nội trợ,nấu,nướng"
entertainingKeywords = "giải trí"
technologyKeywords = "nhân tạo,công nghệ,kỹ thuật"
softwareKeywords = "software,phần mềm,soft"
realestateKeywords = "nhà,đất,động sản,sổ đỏ,sổ hồng,chung cư,tầng,lầu,cầu thang,biệt thự,giấy tờ,chính chủ,quy hoạch,bản đồ,vay vốn,vốn"
furnitureKeywords = "bàn,ghế,giường,kệ tivi,tủ,salon,sofa,kệ trang,đèn,đồng hồ,gối,thảm,tranh,két sắt"
appliancesKeywords = "Nồi cơm điện,Máy Làm Mát,Điều Hòa,Lò vi sóng,Bếp ga,Bếp Âm,Bếp Từ,Hồng Ngoại,Máy hút khói,Nồi áp suất,Máy nóng lạnh,Ấm,Ca,Bình Đun,Máy lọc không khí,Máy xay sinh tố,Bình Thủy Điện,Máy ép trái cây,Máy làm sữa,Máy pha cà phê,Máy Hút Bụi,Bàn Ủi,Quạt,Máy Sấy Tóc,Đồ Dùng Nhà Bếp,Đồ dùng gia đình,Thiết Bị Chiếu Sáng,Nồi,Chảo,Máy nước nóng,Máy Lọc Nước,Bếp Nướng,Bếp gas,Bếp nướng điện,Lẩu điện,Máy đánh trứng,Máy pha cà phê,Máy hút chân không,Lò nướng,Lò vi sóng,Nồi chiên không dầu,Bình đun siêu tốc,Bình thủy điện,Máy hút mùi,Quạt,Quạt sưởi,Cây nước nóng lạnh,Bàn ủi,Máy lọc không khí,Thiết bị làm đẹp,Đèn sưởi,Máy bơm nước,bếp"
autoKeywords = "xe,bánh xe,siêu sang,ô tô,auto,honda,toyota,xe hơi,xe con,bốn bánh,Abarth,Alfa,Romeo,Aston,Martin,Audi,Bentley,BMW,Bugatti,Cadillac,Caterham,Chevrolet,Chrysler,Citroen,Dacia,Ferrari,Fiat,Ford,Honda,Hyundai,Infiniti,Jaguar,Jeep,Kia,Lamborghini,Rover,Lexus,Lotus,Maserati,Mazda,Mclaren,Mercedes-Benz,MG,Mini,Mitsubishi,Morgan,Nissan,Noble,Pagani,Peugeot,Porsche,Radical,Renault,Rolls-Royce,Saab,Seat,Skoda,Smart,SsangYong,Subaru,Suzuki,Tesla,Toyota,Vauxhall,Volkswagen,Volvo,Zenos"
gameKeywords = "trò chơi,game,trò,down,down load,store,android,ios,phiên bản"

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