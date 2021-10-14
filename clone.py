import os
import json
import argparse
import requests

def extractFiles(files, prefix=None):
    file_paths, dir_paths = [], {}
    for k in files:
        for kk in files[k]:
            if prefix is None:
                fn = k
            else:
                fn = '/'.join([prefix, k])
            if kk == 'size':
                file_paths.append(fn)
            else:
                dir_paths[fn] = files[k]
    
    for k in dir_paths:
        file_paths += extractFiles(dir_paths[k], prefix=k)
    
    return file_paths

def downloadFiles(file_url, file_paths, save_dir, ssl_verify=True):
    for fn in file_paths:
        paths = fn.split('/')
        paths.insert(0, save_dir)
        full_name = os.path.join(*paths)

        if len(paths) > 1:
            os.makedirs(os.path.join(*paths[:-1]), exist_ok=True)
        
        url = file_url + fn
        print('Download:', url)
        reply = requests.get(url, verify=ssl_verify)
        if reply.status_code == 200:
            print('Write:', full_name)
            with open(full_name, 'wb') as f:
                f.write(reply.content)
        else:
            print('ERROR:', url, reply.status_code)

def main(save_dir, repo_name, proxy=None, ssl_verify=True):
    if proxy is not None:
        os.environ['http_proxy'] = proxy
        os.environ['https_proxy'] = proxy

    files_url = 'https://anonymous.4open.science/api/repo/{}/files/'.format(repo_name)
    file_url = 'https://anonymous.4open.science/api/repo/{}/file/'.format(repo_name)

    reply = requests.get(files_url, verify=ssl_verify)
    text = reply.text
    files = json.loads(text)
    file_paths = extractFiles(files)

    downloadFiles(file_url, file_paths, save_dir, ssl_verify=ssl_verify)

if __name__ == '__main__':
    argparser = argparse.ArgumentParser('clone.py', description='A small tool to clone all files of a repository in anonymous.4open.science')
    argparser.add_argument('save_dir', help='direcotry to save cloned files')
    argparser.add_argument('repo_name', help='name of a repository in anonymous.4open.science')
    argparser.add_argument('--proxy', '-p', help='Proxy server address')

    args = argparser.parse_args()
    save_dir = args.save_dir
    repo_name = args.repo_name
    proxy = args.proxy
    ssl_verify = True

    main(save_dir, repo_name, proxy, ssl_verify)
