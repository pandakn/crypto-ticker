import pygame
import sys
import requests
from gtts import gTTS
from playsound import playsound
import pyttsx3
import json
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QComboBox, QLabel

engine = pyttsx3.init()

language = 'th'

class CryptoDisplay(QMainWindow):
    def __init__(self):
        self.price = 0
        self.symbol = ''
        super().__init__()
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ["Symbol", "Price", "Market Cap", "Logo"])
        self.setCentralWidget(self.table)

        self.combo = QComboBox(self)
        self.label = QLabel(self)
        self.combo.setGeometry(660, 50, 100, 20)
        self.label.setGeometry(660, 100, 200, 22)
        self.combo.activated[str].connect(self.on_activated)
        self.refresh_data()

    def on_activated(self, text):
        self.label.setText("Selected coin: " + text)
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
        parameters = {
            "start": "1",
            "limit": "20",
            "convert": "THB"
        }
        headers = {
            "Accepts": "application/json",
            "X-CMC_Pro_API_Key": "8bbe9708-84e5-4457-8c09-066db97aef7a"
        }
        response = requests.get(url, headers=headers, params=parameters)
        data = json.loads(response.text)
        # self.table.setRowCount(0)

        # print(text)

        for i, crypto in enumerate(data["data"]):
            self.symbol = crypto["symbol"]
            self.price = crypto["quote"]["THB"]["price"]

            if self.symbol == text:
                self.symbol = self.symbol
                self.price = self.price
                break

        status_code = self.send_price_to_line_notify()

        if status_code == 200:

            my_text = "ราคาของ " + self.symbol + " ส่งเข้าในไลน์แล้วนะจ๊ะ"

            print(my_text)

            my_obj = gTTS(text=my_text, lang=language, slow=False)
            my_obj.save("coin.mp3")
            # playsound("coin.mp3")
            pygame.init()
            pygame.mixer.init()

            filename = "coin.mp3"

            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            pygame.quit()

            # Playing the converted file
            # os.system("mpg321 welcome.mp3")
        else:
            print("Failed to send the price of " + self.symbol)

    def refresh_data(self):
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
        parameters = {
            "start": "1",
            "limit": "20",
            "convert": "THB"
        }
        headers = {
            "Accepts": "application/json",
            "X-CMC_Pro_API_Key": "8bbe9708-84e5-4457-8c09-066db97aef7a"
        }
        response = requests.get(url, headers=headers, params=parameters)
        data = json.loads(response.text)
        self.table.setRowCount(0)

        for i, crypto in enumerate(data["data"]):
            self.symbol = crypto["symbol"]
            self.price = crypto["quote"]["THB"]["price"]
            market_cap = crypto["quote"]["THB"]["market_cap"]
            logo_url = f"https://s2.coinmarketcap.com/static/img/coins/32x32/{crypto['id']}.png"

            self.table.insertRow(i)
            self.table.setColumnWidth(1, 200)
            self.table.setItem(i, 0, QTableWidgetItem(self.symbol))
            self.table.setItem(i, 1, QTableWidgetItem(str(self.price)))
            self.table.setItem(i, 2, QTableWidgetItem(str(market_cap)))
            logo_response = requests.get(logo_url)
            logo_image = QImage.fromData(logo_response.content)
            logo_icon = QIcon(QPixmap.fromImage(logo_image))
            self.table.setItem(i, 3, QTableWidgetItem(''))
            self.table.item(i, 3).setIcon(logo_icon)
            self.combo.addItem(self.symbol)

    def send_price_to_line_notify(self):
        line_notify_token = "qVzjLXTd9U2qbX21IBbzEmX2OkgUuSfr9t512h0jjLA"
        headers = {
            "Authorization": "Bearer " + line_notify_token
        }
        message = "The current price of " + self.symbol + \
            " is: " + str(self.price) + " THB"
        payload = {
            "message": message
        }
        response = requests.post(
            "https://notify-api.line.me/api/notify", headers=headers, data=payload)

        return response.status_code


app = QApplication(sys.argv)
window = CryptoDisplay()
# window.refresh_data()
window.showMaximized()
sys.exit(app.exec_())
