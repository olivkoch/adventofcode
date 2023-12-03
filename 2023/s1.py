import re

datafile = '1.dat'
numbers = [str(x) for x in range(10)]
numinletters = {'one':'1','two':'2','three':'3','four':'4','five':'5','six':'6','seven':'7','eight':'8','nine':'9','zero':'0'}
print(numbers)

with open(datafile,'r') as fp:
    lines = fp.readlines()
    out = 0
    cnt = 0
    for line in lines:
        line = line.strip()
        print(line)
        nms = []
        linerev = line[::-1]
        # left one
        ans = []
        for k,v in numinletters.items():
            ind = line.find(k)
            ans.append((ind,v))
        for i, k in enumerate(numbers):
            ind = line.find(k)
            ans.append((ind,str(k)))
        ans = filter(lambda x:x[0] != -1, ans)
        ans = sorted(ans, key=lambda x:x[0])
        nms.append(ans[0][1])
        # right one
        ans = []
        for k,v in numinletters.items():
            ind = linerev.find(k[::-1])
            ans.append((ind,v))
        for i, k in enumerate(numbers):
            ind = linerev.find(k)
            ans.append((ind,str(k)))
        ans = filter(lambda x:x[0] != -1, ans)
        ans = sorted(ans, key=lambda x:x[0])
        nms.append(ans[0][1])
        print(f'nms = {nms}')
        out += int(nms[0] + nms[-1])
        cnt += 1
    print('done')
    print(out)
    print(cnt)
