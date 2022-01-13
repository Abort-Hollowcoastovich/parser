yaml = open('text2.yml','r', encoding='utf8').read().split('\n')[1:]

def tab(s):
    return '\t'*(s.split('-')[0].count(' ')//2+1) if '- ' == s.strip()[0:2] else "\t"*((s.count(' '))//2)

def nearestBracket(s):
    s = s.split('\n')
    for i in range(len(s)-1, 1, -1):
        if '{' in s[i] and tab(s[i]) != tab(s[i-1]): return '{'
        if '[' in s[i]: return '['

def breacketCounter(s):
    rightcounter = 0
    leftcounter = 0
    s = s.split('\n')[1:]
    for str in s:
        if ':' in str:
            rightcounter += str.split('"')[-1].count('}')
            leftcounter += str.split('"')[-1].count('{')
        elif str.strip() == '{': leftcounter += 1
        elif str.strip() == '},': rightcounter += 1
    return leftcounter - rightcounter

def parseNoKey(str, nextstr):
    tabstr = tab(str)
    str = str.split('-')[1][1:]
    str = str[1:-1] if str[0] == '"' and str[-1] == '"' else str
    if ':' not in nextstr and nextstr.strip()[0] == '-': return tabstr + '"' + str + '",'
    else: return tabstr + '"' + str + '"' + (' ],' if tabstr > tab(nextstr.split(':')[0]) else ',')

def parse(str, json, nextstr, laststr):
    try:
        key = str.split(':')[0]
        if str.split(':')[1] == '':
            value = ''
        else:
            value = str[len(key)+2:]
            value = value[1:-1] if value[0] == '"' and value[-1] == '"' else value
    except: return json + '\n' + parseNoKey(str, nextstr)
    nextkey = nextstr.split(':')[0]
    tabkey = tab(key)
    tabnextkey = tab(nextkey)
    notstr = {'1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.'}
    sjson = tabkey + '"'+ key.strip() + '":' if key.strip()[0] != '-' else tabkey + '"'+key.strip()[2:] + '":'
    if value == '' and nextkey.strip()[0] != '-': sjson += '{'
    elif set(value).issubset(notstr) or value in ['true', 'false', 'null']:
        sjson += ' ' + value + (
            '' if nextkey.strip()[0] == '-' or tabkey > tabnextkey else (',' if str != laststr else ''))
    elif value != '':
        sjson += ' "' + value + '"' + (
            '' if nextkey.strip()[0] == '-' or tabkey > tabnextkey else (',' if str != laststr else ''))
    if nextkey.strip()[0] == '-':
        if tabkey < tabnextkey: sjson += ' [' if ':' not in nextstr and nextstr.strip()[0] == '-' else '[{'
        elif tabkey == tabnextkey: sjson +=  '\n' + tabkey + '},' + '\n' + tabkey + '{'
    if tabkey > tabnextkey:
        if nextstr == '.:.': sjson += ' }]'
        else: sjson += ' },' if nearestBracket(json) == '{' else ' }],'
    return json + '\n' + sjson

def parse1():
    text = open('text.json', 'w', encoding="utf-8")
    json = '{'
    for i in range(len(yaml)-1):
        json = parse(yaml[i], json, yaml[i+1], yaml[len(yaml)-1])
    json = parse(yaml[len(yaml)-1], json, '.:.', yaml[len(yaml)-1], )
    for i in range(breacketCounter(json)):
        json += '\n}'
    text.write(json + '\n}')
    text.close()

parse1()
