import random

from mongoengine import connect

from celos.models import *
import settings as SETTINGS

MAX_ENTRIES = 100

def main():
    if SETTINGS.MONGO['USERNAME']:
        connect(
            SETTINGS.MONGO['NAME'], 
            username = SETTINGS.MONGO['USERNAME'], 
            password = SETTINGS.MONGO['PASSWORD'],
            host = SETTINGS.MONGO['HOST'],
            port = SETTINGS.MONGO['PORT'],
        )
    else:
        connect(
            SETTINGS.MONGO['NAME'],
            host = SETTINGS.MONGO['HOST'],
            port = SETTINGS.MONGO['PORT'],
        )
    

    for i in range(MAX_ENTRIES):
        fake_ip = '{0}.{1}.{2}.{3}'.format(random.randint(0,256), random.randint(0,256), random.randint(0,256), random.randint(0,256))
        user_agents = [
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.120 Chrome/37.0.2062.120 Safari/537.36',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; InfoPath.1; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; Browzar)',
            'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; pl-pl) AppleWebKit/312.8 (KHTML, like Gecko, Safari) DeskBrowse/1.0',
            'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre',
            'Mozilla/5.0 (BlackBerry; U; BlackBerry 9900; en) AppleWebKit/534.11+ (KHTML, like Gecko) Version/7.1.0.346 Mobile Safari/534.11+',
            'Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
            'Mozilla/5.0 (Linux; U; Android 2.3.3; en-us; HTC_DesireS_S510e Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile',
            'Opera/9.80 (J2ME/MIDP; Opera Mini/9.80 (J2ME/22.478; U; en) Presto/2.5.25 Version/10.54',
            'Mozilla/5.0 (PLAYSTATION 3; 3.55)',
        ]
        e = Entry(
            host = Host(ip=fake_ip, user_agent=random.choice(user_agents)),
            lvl = random.randint(1,7),
            msg = 'error test error test',
        ).save()



if __name__ == "__main__":
    main()