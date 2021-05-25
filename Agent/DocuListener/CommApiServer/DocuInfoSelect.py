# api 서버랑 통신하는 모듈

import requests
import hashlib

def SetSearchfile(filepath):
    # f = open("D:/study/network.txt", 'rb')      #파일위치지정 필요
    searchFile = open(filepath,'rb')

    data = searchFile.read()
    sha256 = hashlib.sha256(data).hexdigest()
    sha512 = hashlib.sha512(data).hexdigest()
    md5 = hashlib.md5(data).hexdigest()
    hash = {'sha256': sha256,'sha512': sha512, 'md5':md5}
    searchFile.close()
    
    result = search(hash)
    if result == 2:
        return True            # db에 해쉬값이 존재한다
    elif result == 1:
        return False
    else:
        print("error")

def search(hash):
    # hash = file()
    # print(hash)



    url=f'http://35.233.216.2:5000/search'
    data = {'name' : 'test', 'sha256' : hash['sha256'], 'sha512' : hash['sha512'], 'md5' : hash['md5']}
    res = requests.post(url, json=data)
    flag = res.text
    if flag == "2":   #이게 db에 값이 있는경우
        return True
    elif flag == "1":
        return False
    else:
        print("error")


