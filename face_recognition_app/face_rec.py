# Kütüphaneleri import ederek başlıyoruz
import face_recognition
import cv2

def find_face(images_list,person_name):

    # Resmimizi yüklüyoruz ve encoding bilgisini alıyoruz
    imageEx = face_recognition.load_image_file("images/"+str(images_list[0]))
    imageEx_face_encoding = face_recognition.face_encodings(imageEx)[0]

    # Aranacak olan yüzün encoding bilgilerini ve ismini alıyoruz
    known_face_encodings = [imageEx_face_encoding]
    known_face_names = [person_name]


    face_locations = [] #resmimiz detect edildiğinde locationlarını tutmak için
    face_encodings = [] #encoding bilgilerini tutmak için(feature extration diyebiliriz)
    face_names = []     #isimleri tutmak için
    face_distances= []  #benzerlik oranlarını tutmak için

    # ilk frame'i alıyoruz
    frame = cv2.imread("images/"+str(images_list[1]))

    # yüz tanımayı daha hızlı yapabilmek adına resmimizi yükseklik ve genişliğini 1/4 oranında küçültüyoruz
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)


    # Frame'deki detect edilen her bir yüzün location ve encoding bilgilerini alıyoruz
    face_locations = face_recognition.face_locations(small_frame)
    face_encodings = face_recognition.face_encodings(small_frame, face_locations)

    for face_encoding in face_encodings:
        # Aranan yüz ile bulunan yüzleri karşılaştırıyoruz
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown"

        # 0 ile 1 aralığında benzerlik oranlarını elde ediyoruz
        distance = face_recognition.face_distance(known_face_encodings, face_encoding)

        face_distances.append(distance[0])
        if matches[0]:
            name = known_face_names[0]

        face_names.append(name)#unknown yüzler için




    # Sonuçları görüntülüyoruz
    for (y1, x2, y2, x1), name, distance in zip(face_locations, face_names,face_distances):
        # 1/4 oranında küçülttüğümüz için 4;küçülttüğümüz sayıyla çarpıp gerçek location değerlerini alıyoruz.
        y1 *= 4
        x2 *= 4
        y2 *= 4
        x1 *= 4
        font = cv2.FONT_HERSHEY_DUPLEX # yazı fontu
        overlay = frame.copy() # opacity vermek için gerçek frame'in kopyasını alıyoruz

        if name == "Unknown":
            cv2.putText(frame, "Acc:"+str(round(1-distance,4))+"%", (x1-65, y1-20), font, 2.0, (255, 0, 0),6)
            # belirlenen locationlarda rectangle çiziyoruz
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 3)
            cv2.rectangle(overlay, (x1, y1), (x2, y2), (255, 0, 0),-1)
            opacity = 0.2
            cv2.addWeighted(overlay, opacity, frame, 1-opacity,0, frame)

        else:
            ROI = frame[y1:y2, x1:x2] # İstediğimiz yüzü bulduğumuz zaman kaydediyoruz
            cv2.imwrite("ROI_images/"+str(person_name).split(" ")[0]+".jpg", ROI)
            cv2.putText(frame, "Acc:"+str(round(1-distance,4))+"%", (x1-65, y1 - 20), font, 2.0, (0, 0, 255),6)
            # belirlenen locationlarda rectangle çiziyoruz
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
            cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 0, 255), -1)
            opacity = 0.1
            cv2.addWeighted(overlay, opacity, frame, 1 - opacity, 0, frame)

        if name == "Unknown":
            cv2.rectangle(frame, (x1-100, y2), (x2+150, y2+100), (255, 0, 0),cv2.FILLED)
            cv2.putText(frame, name, (x1, y2 + 80), font, 2.0, (255, 255, 255), 4)
        else:
            cv2.rectangle(frame, (x1-90, y2), (x2+140, y2+100), (0, 0, 255), cv2.FILLED)
            cv2.putText(frame, name, (x1 - 85, y2 + 80), font, 2.0, (255, 255, 255), 4)

    resultName = str(str(images_list[1]).split(".")[0]+"_sonuc.jpg")
    cv2.imwrite("images/"+resultName,frame)
    return resultName