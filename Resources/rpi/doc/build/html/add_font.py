import os

to_add = "<link href='http://fonts.googleapis.com/css?family=PT+Sans' "
to_add += "rel='stylesheet' type='text/css'>\n"


files = os.listdir('.')

for f in files:
    if f.endswith('.html') and f[0] in ['0', 'i']:
        r = open(f, 'r').readlines()
        n = open(f, 'w')
        n.writelines(r[:12])
        n.write(to_add)
        n.writelines(r[12:])
        n.close()