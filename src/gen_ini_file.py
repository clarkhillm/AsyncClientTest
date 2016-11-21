with open('./all_good_ip.txt', 'r') as f:
    txt = f.read()

ips = txt.split('\n')
for ip in ips:
    ip.replace('\n', '')

rs = ''
__ips = []

for x in ips:
    if ips.count(x) >= 1:
        __ips.append(x)

__ips = list(set(__ips))
print len(__ips)

for ip in __ips:
    rs = ip + '|' + rs
print rs
