import requests
import hashlib

def file():
    f = open("D:/study/network.txt", 'rb')      #파일위치지정 필요
    data = f.read()
    sha256 = hashlib.sha256(data).hexdigest()
    sha512 = hashlib.sha512(data).hexdigest()
    md5 = hashlib.md5(data).hexdigest()
    hash = {'sha256': sha256,'sha512': sha512, 'md5':md5}
    f.close()
    #add(hash)
    a = search(hash)
    if a == 2:
        return 2            # db에 해쉬값이 존재한다
    elif a == 1:
        return 1
    else:
        print("error")

    # return hash

def search(hash):
    # hash = file()
    # print(hash)
    url=f'http://35.233.216.2:5000/search'
    data = {'name' : 'test', 'sha256' : hash['sha256'], 'sha512' : hash['sha512'], 'md5' : hash['md5']}
    res = requests.post(url, json=data)
    flag = res.text
    if flag == "2":         #이게 db에 값이 있는경우
        return 2
    elif flag == "1":
        return 1
    else:
        print("error")

def add(hash):
    # hash = file()
    # print(hash)
    url=f'http://35.233.216.2:5000/add'
    #파일이름, 파일형식 정보 받아와야됨(name, extension)
    data = {'name' : 'test', 'sha256' : hash['sha256'], 'sha512' : hash['sha512'], 'md5' : hash['md5'], 'extension' : 'txt'}
    res = requests.post(url, json=data)
    flag = res.text
    if flag == "Insert Success":
        return 2
    elif flag == "Insert Fail":
        return 1


file()


