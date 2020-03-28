all = ''
with open('Discussion.txt') as file:
    while True:
        text = file.readline()
        if len(text) == 0:
            break
        text = text.split(':')
        if len(text)>2:
            text[2] = text[2][1:]
        for t in text[2:]:
            if t != ' <médias omis>':
                all += t

all = all.lower()
olds = ['ç', 'à', 'é', 'è', 'œ']
news = ['c', 'a', 'e', 'e', 'oe']
for old, new in zip(olds, news):
    all = all.replace(old, new)

char = [' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', "'", ',', '.', '?', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
alltxt = ''
for t in all:
    if t in char:
        alltxt += t

with open('DiscussionCorrect.txt', 'w') as file:
    file.write(alltxt)