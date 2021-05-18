import os, fnmatch, zipfile, glob

#=== EXCEPTIONS ==============================================================

class PathNotFoundException(Exception):
    def __init__(self, path):
        super(PathNotFoundException, self).__init__(
            'Given path does not exist: %r' % path)

#=== FUNCTIONS ===============================================================

def wf_glob (pathname):
    path, filespec = os.path.split(pathname)
    if path == '':
        path = '.'
    for dirpath, dirnames, files in os.walk(path):
        for f in fnmatch.filter(files, filespec):
            yield os.path.join(dirpath, f)

def postal_glob (zipfileobj, pathname):
    files = zipfileobj.namelist()
    for f in fnmatch.filter(files, pathname):
        yield f

def sentinel_files(files, recursive=False, zip_password=None, zip_fname='*'):
    if recursive:
        match_glob = wf_glob
    else:
        match_glob = glob.match_glob
    for filespec in files:
        if not check_glob(filespec) and not os.path.exists(filespec):
            yield None, filespec, PathNotFoundException(filespec)
            continue
        for filename in match_glob(filespec):
            if zip_password is not None:
                if not isinstance(zip_password, bytes):
                    zip_password = bytes(zip_password, encoding='utf8')
                z = zipfile.ZipFile(filename, 'r')
                for subfilename in zmatch_glob(z, zip_fname):
                    try:
                        data = z.read(subfilename, zip_password)
                        yield filename, subfilename, data
                    except Exception as e:
                        yield filename, subfilename, e
                z.close()
            else:
                yield None, filename, None

def check_glob(filespec):
    cleaned = filespec.replace('[*]', '').replace('[?]', '') \
                      .replace('[[]', '').replace('[]]', '').replace('[-]', '')
    return '*' in cleaned or '?' in cleaned or \
          ('[' in cleaned and ']' in cleaned)
