# El takip uygulamasi

import cv2
import time
import mediapipe as mp

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

# Ekrana FPS degerlerini yazmak:
pTime = 0 # gecmis zaman
cTime = 0 # simdiki zaman

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks) # el koordinatlarini yazdirir. EL gormez ise None yazacaktir.

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                #print(id,lm)
                # Yukaridaki print islemi ile koordinatlari ondalikli olarak aliyoruz.
                # Piksel seklinde alabilmek icin h,w kullanimi:
                # yukseklik, genislik ve kanallari
                h,w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                print(id, cx, cy)
                # bilek noktasina bir nokta koyalim:
                if id == 0:

                   # 0 : bilek noktasi
                   # 4 : bas parmak ucu
                   # 8 : isaret parmagi ucu
                   # 12: orta parmak ucu
                   # 16: yuzuk parmak ucu
                   # 20: serce parmak ucu

                   # Eger tum noktalari belirginlestirmek istersek if yorum satirina cevrilir. alttaki satir if ile ayni hizaya alinir.
                    cv2.circle(img, (cx,cy), 10, (0,150,255), cv2.FILLED)

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            # handLms ile 21 noktayi ve hand_connec ile de bu noktalari birbirine baglayan cizgiler cizilir.

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    # Ekrana yazi yazdirma:
    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)



    cv2.imshow('Image',img)
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break
