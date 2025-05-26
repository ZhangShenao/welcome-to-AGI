# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/24 14:06 
@Author  : ZhangShenao 
@File    : upload_image.py 
@Desc    : 上传图片
"""

import http.client
import mimetypes
from codecs import encode

conn = http.client.HTTPSConnection("app-api.pixverse.ai")
dataList = []
boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=image; filename={0}'.format('')))

fileType = mimetypes.guess_type('')[0] or 'application/octet-stream'
dataList.append(encode('Content-Type: {}'.format(fileType)))
dataList.append(encode(''))

with open('', 'rb') as f:
    dataList.append(f.read())
dataList.append(encode('--' + boundary + '--'))
dataList.append(encode(''))
body = b'\r\n'.join(dataList)
payload = body
headers = {
    'API-KEY': '',
    'Ai-trace-id': '{{$string.uuid}}',
    'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
}
conn.request("POST", "/openapi/v2/image/upload", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
