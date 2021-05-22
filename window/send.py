import requests
import hashlib

def file():
    f = open("D:/study/network.txt", 'rb')
    data = f.read()
    sha256 = hashlib.sha256(data).hexdigest()
    sha512 = hashlib.sha512(data).hexdigest()
    md5 = hashlib.md5(data).hexdigest()
    hash = {'sha256': sha256,'sha512': sha512, 'md5':md5}
    f.close()
    #add(hash)
    search(hash)
    # return hash

def search(hash):
    # hash = file()
    # print(hash)
    url=f'http://35.233.216.2:5000/search'
    data = {'name' : 'test', 'sha256' : hash['sha256'], 'sha512' : hash['sha512'], 'md5' : hash['md5']}
    res = requests.post(url, json=data)
    flag = res.text
    if flag == "2":         #이게 db에 값이 있는경우
        print (res.text)
    else:
        print("a")

def add(hash):
    # hash = file()
    # print(hash)
    url=f'http://35.233.216.2:5000/add'
    data = {'name' : 'test', 'sha256' : hash['sha256'], 'sha512' : hash['sha512'], 'md5' : hash['md5'], 'extension' : 'txt'}
    res = requests.post(url, json=data)
    flag = res.text
    print(flag)

file()


