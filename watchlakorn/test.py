import requests
from bs4 import BeautifulSoup
import lxml
import lxml.html
import json
import os
import datetime

headers_mobile = { 'User-Agent' : 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B137 Safari/601.1'}
headers_postman = {
    # 'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'referer' : 'https://www.watchlakorn.in/OMG%E0%B8%9C%E0%B8%B5%E0%B8%9B%E0%B9%88%E0%B8%A7%E0%B8%99%E0%B8%8A%E0%B8%A7%E0%B8%99%E0%B8%A1%E0%B8%B2%E0%B8%A3%E0%B8%B1%E0%B8%81%E0%B8%95%E0%B8%AD%E0%B8%99%E0%B8%97%E0%B8%B5%E0%B9%885%E0%B8%A7%E0%B8%B1%E0%B8%99%E0%B8%97%E0%B8%B5%E0%B9%888%E0%B8%95%E0%B8%B8%E0%B8%A5%E0%B8%B2%E0%B8%84%E0%B8%A12561-video-243982',
    # 'Cache-Control' : 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0',
    # 'Connection' : 'keep-alive',
    # 'Content-Encoding' : 'gzip',
    # 'Content-Length' : '154',
    # 'Content-Type' : 'text/html; charset=TIS-620',
    # 'Keep-Alive' : 'timeout=60',
    # 'Pragma' : 'no-cache',
    # 'Server' : 'nginx',
    # 'Vary' : 'Accept-Encoding',
    # 'X-Powered-By' : 'PHP/5.6.40'
}


def getCodeKt(content):
    video = content.find(id="videoclip")
    code_kt = video.find('p').get('id')

    return code_kt


def getCodeV(content):
    root = lxml.html.fromstring(content)
    meta = root.xpath("//meta[@property='og:video:url']/@content")[0]

    index = meta.rfind('/')

    return meta[index + 1:]


def getPlayList(url):
    headers = {'referer' : url}
    re = requests.get(url, headers=headers_mobile)
    content = BeautifulSoup(re.content, 'lxml')
    code_kt = getCodeKt(content)
    code_v = getCodeV(re.content)

    url2 = "http://www.watchlakorn.in/content_jw6.php?v=" + code_v + "&kt=" + code_kt
    print(url2)
    re2 = requests.get(url2, headers=headers)
    content = re2.content

    file = json.loads(content)

    url_play_list = "https:" + (file[0]['file'])
    print(url_play_list)
    re3 = requests.get(url_play_list, headers=headers)
    content = re3.content
    arr = str(content).split('\\n')

    result = []
    for item in arr:
        if '.ts' in item:
            result.append(item)

    return result


def delete_all_video():
    pwd = os.getcwd() + '\\downloads\\'

    filelist = os.listdir(pwd)
    list_file_delete_1 = []
    for fichier in filelist[:]:
        if (fichier.endswith('.ts')):
            list_file_delete_1.append(fichier)

    for file in list_file_delete_1:
        os.remove(pwd + file)


def get_video(url, file_name):
    path_file = ".ts"
    r = requests.get(url, stream=True)  # create HTTP response object
    with open("downloads\\" + str(file_name) + str(path_file), 'wb') as f:
        for chunk in r.iter_content(chunk_size=2048):
            if chunk:
                f.write(chunk)
    return 'done'


if __name__ == "__main__":
    # url = str(input("Enter url video: "))
    url = "https://www.watchlakorn.in/%E0%B8%81%E0%B8%A5%E0%B8%A5%E0%B8%A7%E0%B8%87%E0%B8%97%E0%B8%A7%E0%B8%87%E0%B8%AB%E0%B8%99%E0%B8%B5%E0%B9%89%E0%B8%A3%E0%B8%B1%E0%B8%81%E0%B8%95%E0%B8%AD%E0%B8%99%E0%B8%97%E0%B8%B5%E0%B9%884%E0%B8%A7%E0%B8%B1%E0%B8%99%E0%B8%97%E0%B8%B5%E0%B9%8815%E0%B8%81%E0%B8%B8%E0%B8%A1%E0%B8%A0%E0%B8%B2%E0%B8%9E%E0%B8%B1%E0%B8%99%E0%B8%98%E0%B9%8C2562-video-262570"

    start = datetime.datetime.now()

    result = getPlayList(url)
    print("Downloading...")
    for i in range(len(result)):
        if i > 20:
            break
        os.system('youtube-dl ' + result[i] + ' --output downloads\\' + str(i + 1) + '.%(ext)s')
        print(i)
        # get_video(result[i], str(i + 1))

    # os.system('youtube-dl -ciw -o "downloads\\%(autonumber)s.%(ext)s" --batch-file="batch-file.txt"')
    #0:01:45.883288
    string = ''
    for i in range(20 + 1):
        string = string + 'downloads\\' + '' + str(i + 1) + '.ts' + '|'

    os.system('ffmpeg -i "concat:' + string + '" -c copy -bsf:a aac_adtstoasc input.mp4')
    delete_all_video()
    os.system('ffmpeg -ss 00:00:50 -y -i "input.mp4"  -i 556330.png -filter_complex "[0:v]eq=brightness=0.05:contrast='
              '0.8:saturation=2:gamma_b=1.0,pad=iw+4:ih+4:2:2:color=white, scale=566:340[v1];movie=xoabg.mp4:loop=999,'
              'setpts=N/(FRAME_RATE*TB), scale = 854:480, setdar =16/9[v2];[v2][v1]overlay=shortest=1:x=-10:y=-10 [v3];'
              '[1:v]scale=854:480 [v4];[v3][v4]overlay=0:0,drawtext=fontfile=fonts/Helvetica-Bold.ttf:text=Please subscr'
              'iber my channel:fontcolor=white:fontsize=36:x=w/10*mod(t\,20):y=400,setdar=16/9;[0:a]aformat=sample_'
              'fmts=fltp:sample_rates=44100:channel_layouts=stereo,atempo=9/10,asetrate=10/9*44100,lowpass=f=3500,high'
              'pass=f=1500,treble=g=16,bass=frequency=110:gain=-50,bass=g=3:f=110:w=1,bass=g=3:f=110:w=2,bass=g=3:f='
              '110:w=3,bass=g=3:f=110:w=4,bass=g=3:f=110:w=5,bass=g=-90,equalizer=f=10.5:width_type=o:width=3:g=-30'
              ', equalizer=f=31.5:width_type=o:width=3:g=-30,equalizer=f=63:width_type=o:width=3:g=-30, equalizer=f='
              '100:width_type=o:width=3:g=-20,equalizer=f=250:width_type=o:width=3:g=-20,equalizer=f=500:width_type='
              'o:width=3:g=-20,equalizer=f=1000:width_type=o:width=3:g=-20,equalizer=f=8000:width_type=o:width=3:g=-3'
              '0,equalizer=f=16000:width_type=o:width=3:g=-30,volume=6,volume=+15dB[a1];[a1]volume=28" -vcodec libx2'
              '64 -pix_fmt yuv420p -r 31 -g 62 -b:v 1800k -shortest -acodec aac -b:a 128k -ar 44100 -metadata album_'
              'artist="" -metadata album="" -metadata date="" -metadata track="" -metadata genre="" -metadata publi'
              'sher="" -metadata encoded_by="" -metadata copyright="" -metadata composer="" -metadata performer="" -m'
              'etadata TIT1="" -metadata TIT3="" -metadata disc="" -metadata TKEY="" -metadata TBPM="" -metadata langu'
              'age="eng" -metadata encoder="" -threads 0 -preset veryfast "output.mp4')

    end = datetime.datetime.now()

    print(end - start)

