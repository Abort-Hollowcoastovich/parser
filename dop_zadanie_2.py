import re

yaml = open('text','r', encoding='utf8').read().split('\n')[1:]

def tab(s):
    return '\t'*(s.split('-')[0].count(' ')//2+1) if re.fullmatch(r'- .*', s.strip()) else "\t"*((s.count(' '))//2)

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
        if re.fullmatch(r'.*:.*', str):
            rightcounter += str.split('"')[-1].count('}')
            leftcounter += str.split('"')[-1].count('{')
        elif str.strip() == '{': leftcounter += 1
        elif str.strip() == '},': rightcounter += 1
    return leftcounter - rightcounter

def parseNoKey(str, nextstr):
    tabstr = tab(str)
    str = str.split('-')[1][1:]
    str = str[1:-1] if re.fullmatch(r'".*"', str) else str
    if re.fullmatch(r'- [^:]*', nextstr.strip()): return tabstr + '"' + str + '",'
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
    sjson = tabkey + '"'+ key.strip() + '":' if re.fullmatch(r'[^-].*', key.strip()) else tabkey + '"'+key.strip()[2:] + '":'
    if value == '' and re.fullmatch(r'[^-].*', nextkey.strip()): sjson += '{'
    elif re.fullmatch(r'[0-9.]+', value) or value in ['true', 'false', 'null']:
        sjson += ' ' + value + (
            '' if re.fullmatch(r'-.*', nextkey.strip()) or tabkey > tabnextkey else (',' if str != laststr else ''))
    elif value != '':
        sjson += ' "' + value + '"' + (
            '' if re.fullmatch(r'-.*', nextkey.strip()) or tabkey > tabnextkey else (',' if str != laststr else ''))
    if re.fullmatch(r'-.*', nextkey.strip()):
        if tabkey < tabnextkey: sjson += ' [' if not re.fullmatch(r'- \S*: .*', nextstr.strip()) else '[{'
        elif tabkey == tabnextkey: sjson +=  '\n' + tabkey + '},' + '\n' + tabkey + '{'
    if tabkey > tabnextkey:
        if nextstr == '.:.': sjson += ' }]'
        else: sjson += ' },' if nearestBracket(json) == '{' else ' }],'
    return json + '\n' + sjson

def parse1():
    json = '{'
    for i in range(len(yaml)-1):
        json = parse(yaml[i], json, yaml[i+1], yaml[len(yaml)-1])
    json = parse(yaml[len(yaml)-1], json, '.:.', yaml[len(yaml)-1], )
    for i in range(breacketCounter(json)):
        json += '\n}'
    text = open('text.json', 'w', encoding="utf-8")
    text.write(json + '\n}')
    text.close()
parse1()