import requests
import re


response = requests.get('https://vt.tiktok.com/ZSN5NGVTE')
html_content = response.text

video_id_math = re.search(r'"id":"(\d+)"', html_content)
if video_id_math:
    video_id = video_id_math.group(1)
    print('ID videos:', video_id)
else:
    print('ID видео найден')



# result = response.text
# with open('result.html', 'w', encoding='utf-8') as html:
#     html.write(result)