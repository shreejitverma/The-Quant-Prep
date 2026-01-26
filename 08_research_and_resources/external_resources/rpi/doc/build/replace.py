import os

rpl = {
    '65p6tn4p8i': 'token',
    'hilpisch13': 'username',
    'henrynikolaus06': 'password',
    'rpi@hilpisch.com': 'rpi@mydomain.net',
    'yves@hilpisch.com': 'me@mydomain.net',
    'ftp://rpi:pythonquants@quant-platform.com': 'ftp://user:password@mydomain.net',
    'smtp.hilpisch.com': 'smtp.mydomain.net'
}

path = './html/'
files = os.listdir(path)

for path, dirs, files in os.walk(path):
    for f in files:
        print path + '/' + f
        if f.endswith('.html') or f.endswith('.py') \
        or f.endswith('.conf') or f.endswith('.txt'):
            r = open(path + '/' + f, 'r').readlines()
            e = []
            for l in r:
                for k, v in rpl.items():
                    l = l.replace(k, v)
                e.append(l)
            # r = [[l.replace(k, v) for k, v in rpl.items()] for l in r]
            n = open(path + '/' + f, 'w')
            n.writelines(e)
            n.close()

for f in files:
    if f.endswith('.html_old'):
        os.remove(f)