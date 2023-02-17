from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT
import time
from speech import audio
from datetime import datetime
import time
import requests
import json
import os

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=4, block_orientation=-
                 90, blocks_arranged_in_order=True)
device.contrast(16)

a = audio()
# a="Hello"

now = datetime.now()
dt1_string = now.strftime("%H:%M:%S")

err = 0


def test():
    while True:
        with canvas(device) as draw:
            url = f"https://api.coingecko.com/api/v3/coins/{a.lower()}?localization=false"
            headers = {'X-Auth-Token': 'YOUR_API_KEY'}
            response = requests.get(url, headers=headers)

            if a == "what time is it":
                show_message(device, dt1_string, fill="red",
                             font=(TINY_FONT), scroll_delay=0.09)
            else:
                if (response.status_code == 200):
                    data = response.json()
                    #currency = data['id']
                    price_thb = data['market_data']['current_price']['thb']
                    #last_date = data['last_updated']
                    #img_currency = data['image']['large']
                    show_message(device, str(price_thb) + " Baht",
                                 fill="red", font=(CP437_FONT), scroll_delay=0.07)

                else:
                    show_message(device, 'Coin not found', fill="red",
                                 font=(CP437_FONT), scroll_delay=0.07)
                    continue


test()
# while True:
#res = test()
#show_message(device, res, fill="red",font=(CP437_FONT),scroll_delay=0.09)
# if a == 'stop':
#os.system('sudo pkill -f /home/os/max7219voicecontrol/ledmatrix2.py')
#show_message(device, a, fill="red",font=(TINY_FONT),scroll_delay=0.09)
