import requests
import hashlib

def add(filepath):
    # hash = file()
    # print(hash)
    url=f'http://35.233.216.2:5000/add'
    #파일이름, 파일형식 정보 받아와야됨(name, extension)


    
    searchFile = open(filepath,'rb')

    data = searchFile.read()
    sha256 = hashlib.sha256(data).hexdigest()
    sha512 = hashlib.sha512(data).hexdigest()
    md5 = hashlib.md5(data).hexdigest()
    hash = {'sha256': sha256,'sha512': sha512, 'md5':md5}
    searchFile.close()


    filename = filepath.split("\\")[-1]
    ext = filename.split(".")[-1]

    data = {'name' : filename, 'sha256' : hash['sha256'], 'sha512' : hash['sha512'], 'md5' : hash['md5'], 'extension' : ext}
    res = requests.post(url, json=data)
    flag = res.text
    if flag == "Insert Success":
        return 2
    elif flag == "Insert Fail":
        return 1
