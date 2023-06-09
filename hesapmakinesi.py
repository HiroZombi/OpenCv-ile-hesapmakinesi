from cvzone.HandTrackingModule import HandDetector #Yapan güncelleyen Ertem K.
import cv2
import time
import pyttsx3


class Button:
    def __init__(self, pos, width, height, value):
        self.pos = pos  # buton konumu
        self.width = width  # buton genişliği
        self.height = height  # buton yüksekliği
        self.value = value  # buton üzerinde yazan değer

    def draw(self, img):
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (0, 0, 0), cv2.FILLED)  # buton arka planı
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (0, 0, 0), 5)  # buton çerçevesi
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width - 8, self.pos[1] + self.height - 7),
                      (51, 51, 42), 5)  # buton kenar çizgisi
        cv2.putText(img, self.value, (self.pos[0] + 30, self.pos[1] + 70), cv2.FONT_HERSHEY_PLAIN,
                    2, (255, 255, 255), 2)  # buton üzerindeki değer yazısı

    def checkClick(self, x, y):
        if self.pos[0] < x < self.pos[0] + self.width and \
                self.pos[1] < y < self.pos[1] + self.height:
            cv2.rectangle(img, (self.pos[0] + 3, self.pos[1] + 3),
                          (self.pos[0] + self.width - 3, self.pos[1] + self.height - 3),
                          (255, 255, 255), cv2.FILLED)  # buton arka planı beyaz renge dönüştürülür
            cv2.putText(img, self.value, (self.pos[0] + 25, self.pos[1] + 80), cv2.FONT_HERSHEY_PLAIN,
                        5, (0, 0, 0), 5)  # buton üzerindeki değer yazısı değiştirilir
            return True  # butona tıklama gerçekleşir
        else:
            return False  # butona tıklama gerçekleşmez


# Butonların listesi ve konumları
buttonListValues = [['exit', 'C', '%', 'sil', '!'],
                    ['**', '7', '8', '9', '*'],
                    ['//', '4', '5', '6', '-'],
                    ['000', '1', '2', '3', '+'],
                    ['00', '0', '/', '.', '=']]
buttonList = []
for x in range(5):
    for y in range(5):
        xpos = x * 100 + 750
        ypos = y * 100 + 120

        buttonList.append(Button((xpos, ypos), 100, 100, buttonListValues[y][x]))

# Değişkenlerin tanımlanması
myEquation = ''
delayCounter = 0
# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8, maxHands=1)

engine = pyttsx3.init() #yazıları konuşturmak için modül

while True:
    # Kameradan görüntü alınması
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)

    # Butonların ve ekrandaki hesaplamaların görselleştirilmesi
    cv2.rectangle(img, (750, 20), (750 + 400, 20 + 100), (255, 255, 255), cv2.FILLED)

    cv2.rectangle(img, (750, 20), (750 + 400, 20 + 100),
                  (51, 51, 42), 10)
    for button in buttonList:
        button.draw(img)


    # Faktöriyel fonksiyonunun tanımlanması
    def fact(n):
        fact1 = 1
        for i in range(1, n + 1):
            fact1 = fact1 * i
        return (fact1)


    # Elleri kontrol et
    if hands:
        # Parmaklar arasındaki mesafeyi bul
        lmList = hands[0]['lmList']
        length, _, img = detector.findDistance(lmList[8], lmList[4], img)
        print(length)
        x, y = lmList[8]

        fingers = detector.fingersUp(hands[0])

        if fingers == [0, 0, 0, 0, 0]:
            print("yumruk")
            engine.say("Exit Time!")
            time.sleep(0.3)
            engine.runAndWait()
            quit()

        if fingers == [1, 1, 0, 0, 1]:
            myEquation = 'spiderman'
            time.sleep(0.3)

        # Tıklanırsa, hangi düğmeye tıklandığını kontrol et ve işlem yap
        if length < 35 and delayCounter == 0:
            for i, button in enumerate(buttonList):
                if button.checkClick(x, y):
                    myValue = buttonListValues[int(i % 5)][int(i / 5)]  # doğru sayıyı al
                    if myValue == 'exit':
                        engine.say("Exit Time")
                        time.sleep(0.3)
                        engine.runAndWait()
                        quit()
                        cv2.destroyAllWindows()
                    if myValue == '=':
                        myEquation = str(eval(myEquation))
                        #eşitliğe tıklandıysa işlem yap
                        engine.say("Equal")
                        time.sleep(0.3)
                        engine.runAndWait()


                    if myValue == '+':
                        engine.say("to collect")
                        time.sleep(0.3)
                        engine.runAndWait()

                    if myValue == '-':
                        engine.say("extraction")
                        time.sleep(0.3)
                        engine.runAndWait()

                    if myValue == '*':
                        engine.say("impact")
                        time.sleep(0.3)
                        engine.runAndWait()

                    elif myValue == 'C':
                        myEquation = ''  # C'ye tıklandıysa denklemi sıfırla
                        engine.say("All Clear")
                        time.sleep(0.3)
                        engine.runAndWait()

                    elif myValue == 'sil':
                        myEquation = myEquation[0:len(myEquation) - 1]  # <'ye tıklandıysa son karakteri sil
                        engine.say("Delete")
                        time.sleep(0.3)
                        engine.runAndWait()
                    elif myValue == '!':
                        myEquation = myEquation[0:len(myEquation)]
                        myEquation = str(fact(int(myEquation)))  # !'ye tıklandıysa faktöriyel hesapla
                        time.sleep(0.3)
                    else:
                        myEquation += myValue  # sayıya tıklandıysa denklemi güncelle
                    delayCounter = 1

    # Birden fazla tıklamayı önlemek için
    if delayCounter != 0:
        delayCounter += 1
        if delayCounter > 10:
            delayCounter = 0

    # Son cevabı yaz
    cv2.putText(img, myEquation, (760, 100), cv2.FONT_HERSHEY_PLAIN,
                3, (0, 0, 0), 3)

    # Göster
    key = cv2.waitKey(1)
    cv2.imshow("Image", img)
    if key == ord('q'):
        myEquation = ''
        break
