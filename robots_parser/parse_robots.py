import json
from urllib.request import urlopen
from time import sleep


def site_avaliable(site):
    try:
        urlopen(site)
    except:
        return False
    else:
        if urlopen(site).getcode() == 200:
            return True
        else:
            return False


def get_robots(url, wait):
    data = ''
    for i in ['http://'+url,'http://www.'+url,'https://'+url,'https://www.'+url]:
        if site_avaliable(i+'/robots.txt'):
            sleep(wait)
            with urlopen(i + '/robots.txt') as resp:
                data += resp.read().decode('utf-8')
            break
    return data


def parse_data(data):
    robots = {}
    for line in data.split('\n'):
        line = line.rstrip('\n')
        if line.lower().startswith('user-agent:'):
            agent = line[len('user-agent: '):]
            robots[agent] = {'allow':[],'disallow':[],'other':[]}
        else:
            while not line.lower().startswith('user-agent:'):
                if line.lower().startswith('allow:'):
                    robots[agent]['allow'].append(line[len('allow:'):].strip())
                elif line.lower().startswith('disallow:'):
                    robots[agent]['disallow'].append(line[len('disallow:'):].strip())
                elif line:
                    try:
                        robots[agent]['other'].append(line.strip())
                    except:
                        pass
                break

    return robots


def create_json(head, robots_dict):
    if robots_dict:
        with open('{}.json'.format(head), 'w') as j:
            json.dump(robots_dict, j, indent=4)


if __name__ == '__main__':
    sites = ['google.com', 'facebook.com', 'vk.com', 'yandex.ru', 'qq.com', '2ch.hk', 'twitter.com', 'twitch.tv',
             'baidu.com', 'etrgrtgrtg.erfk']
    wait = 1
    for each in sites:
        robots = parse_data(get_robots(each, wait))
        create_json(each, robots)