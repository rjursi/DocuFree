# api 서버랑 통신하는 모듈

import requests
import hashlib


def ChangePathFormat(filepath):
    
    new_pathFormat = filepath.replace("\\","/").replace("//","/").replace("\'","").replace("\"","")
    
    return new_pathFormat


def SetSearchFile(filepath):

    filepath = ChangePathFormat(filepath)
    
    print(filepath)

    

    with open(filepath,'rb+') as searchFile:

        data = searchFile.read()

        sha256 = hashlib.sha256(data).hexdigest()
        sha512 = hashlib.sha512(data).hexdigest()
        md5 = hashlib.md5(data).hexdigest()
        hash = {'sha256': sha256,'sha512': sha512, 'md5':md5}

        result = search(hash)


        if result:
            return True            # db에 해쉬값이 존재한다
        else:
            return False

def search(hash):

    url=f'http://35.233.216.2:5000/search'
    data = {'name' : 'test', 'sha256' : hash['sha256'], 'sha512' : hash['sha512'], 'md5' : hash['md5']}
    res = requests.post(url, json=data)
    flag = res.text
    print(flag)
    if flag == "Found":   #이게 db에 값이 있는경우
        return True
    elif flag == "Not Found":
        return False


