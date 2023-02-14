import sys
import requests
import json
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel
from PyQt5.QtGui import QImage, QPixmap, QIcon, QFont

class CryptoCard(QLabel):
    def __init__(self, symbol, price, logo_url, parent=None):
        super().__init__(parent)

        self.setFixedSize(100, 200)

        logo_response = requests.get(logo_url)
        logo_image = QImage.fromData(logo_response.content)
        logo_icon = QIcon(QPixmap.fromImage(logo_image))

        self.setPixmap(logo_icon.pixmap(80, 80))
        self.symbol = QLabel(symbol, self)
        self.symbol.setGeometry(0, 120, 120, 20)
        self.symbol.setFont(QFont("Inter", 12, weight=QFont.Bold))
        self.price_label = QLabel(price, self)
        self.price_label.setFont(QFont("Inter", 14, weight=QFont.Bold))
        self.price_label.setGeometry(0, 150, 120, 20)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.grid = QGridLayout(self)
        self.grid.setSpacing(10)

        self.refresh_data()

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

        for i, crypto in enumerate(data["data"]):
            symbol = crypto["symbol"]
            price = f"฿{crypto['quote']['THB']['price']:.2f}"
            logo_url = f"https://s2.coinmarketcap.com/static/img/coins/64x64/{crypto['id']}.png"

            card = CryptoCard(symbol, price, logo_url)
            self.grid.addWidget(card, i // 4, i % 4)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())
