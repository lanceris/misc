import json
import os
import re
from urllib.request import urlopen, Request


def check_site(site,user_agent=None):
    avaliable = False
    if user_agent:
        headers = {'User-Agent': USER_AGENT}
        req = Request(site, headers=headers)
    else:
        req = urlopen(site)
    try:
        page_open = urlopen(req)
    except:
        pass
    else:
        avaliable = True
    finally:
        return avaliable


def get_robots_txt(url):
    robots1 = 'http://'+url+'/robots.txt'
    robots2 = 'https://' + url + '/robots.txt'
    if check_site(robots1):
        with urlopen(robots1) as resp:
            return resp.read()
    if check_site(robots2):
        with urlopen(robots2) as resp:
            return resp.read()


def save_to_txt(txt,data):
    if data:
        with open(txt, 'w') as file_to_write:
            file_to_write.write(data.decode('utf-8'))
    else:
        print('There is nothing to save.')


def parse_txt(txt):
    robots = {}
    txt += '.txt'
    if os.path.isfile(txt):
        with open(txt, 'r') as f:
            for line in f:
                line = line.rstrip('\n')
                if line.lower().startswith('user-agent:'):
                    agent = line[len('user-agent:'):].lstrip(' ')
                    robots[agent] = {'allow':[],'disallow':[],'other':[]}
                else:
                    while not line.lower().startswith('user-agent:'):
                        if line == '\n':
                            break
                        if line.lower().startswith('allow:'):
                            try:
                                robots[agent]['allow'].append(line[len('allow:'):].strip())
                            except:
                                pass
                        elif line.lower().startswith('disallow:'):
                            try:
                                robots[agent]['disallow'].append(line[len('disallow:'):].strip())
                            except:
                                pass
                        elif line:
                            try:
                                robots[agent]['other'].append(line.strip())
                            except:
                                pass
                        break

        return robots

    else:
        print('No such file!')


def get_json(url):
    site = re.search(r'(.*)\.*', url)
    site = site.group(0)
    print()
    print(site)
    if not os.path.isfile(os.path.join(os.curdir,site+'.json')):
        print('It\'s a new site, creating {}.json...'.format(site))
        data = get_robots_txt(url)
        save_to_txt('{}.txt'.format(site), data)
        with open(site+'.json','w') as f:
            json.dump(parse_txt(site),f, sort_keys=True, indent=4)
        clean_up(mode='t')
        return 'Success'
    else:
        return 'File already exists'


def get_allowed_links():
    pass


def clean_up(dire=os.curdir,mode='t'):
    for name in os.listdir(dire):
        if mode == 't':
            if name.endswith('.txt'):
                os.remove(name)
        elif mode == 'j':
            if name.endswith('.json'):
                os.remove(name)


def main(sites,user_agent=None):
    while 1:
        print('\n\tHello!')
        print('1 - get .json files for sites\n'
              '2 - delete all .json files\n'
              '3 - exit')
        choice = input('Please choose option: ')
        if choice == '1':
            for each in sites:
                get_json(each)
            print('\nAll done.')
        elif choice == '2':
            clean_up(mode='t')
            clean_up(mode='j')
            print('All files deleted.')
        elif choice == '3':
            print('Good bye!')
            break
        else:
            print('Wrong choice!')


if __name__ == '__main__':
    USER_AGENT = r'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    sites = ['google.com', 'facebook.com', 'vk.com', 'yandex.ru', 'qq.com', '2ch.hk', 'twitter.com', 'twitch.tv',
             'baidu.com', 'etrgrtgrtg.erfk']
    main(sites=sites,user_agent=USER_AGENT)