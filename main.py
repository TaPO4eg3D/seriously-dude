import json

import base64
from io import BytesIO

from urllib import request
from urllib.error import HTTPError, URLError

import datetime

from PIL import Image

MS_TEAMS_URL = ''

CURRENT_DAY = datetime.datetime.now().date()
TARGET_DAY = datetime.datetime.fromisoformat('2022-09-03').date()

if CURRENT_DAY >= TARGET_DAY:
    raise RuntimeError()

STEP = 15
MOVABLE_WIDTH = 194

OFFSET = (TARGET_DAY - CURRENT_DAY).days * STEP

background = Image.new(
    mode='RGB', size=(480, 546), color='white',
)

movable_part = Image.open("movable_part.png")
movable_part.convert('RGBA')

background.paste(movable_part, (-OFFSET, 0), movable_part)

buffered = BytesIO()
background.save(buffered, format="JPEG")
img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

payload = {
    "@type": "MessageCard",
    "text": "",
    "sections": [
        {
            "images": [
                {
                    "image": f"data:image/png;base64,{img_str}"
                }
            ]
        }
    ]
}

request_data = json.dumps(payload).encode('utf-8')
req = request.Request(MS_TEAMS_URL, data=request_data)

try:
    response = request.urlopen(req)
    print(response.__dict__)
except (HTTPError or URLError) as e:
        print(e)
