from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext.filters import Filters
import telegram
import random
import subprocess
import logging
import wikipediaapi
import json
import requests
import datetime

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

photos = {
        "metacircular": 'AgADBQADV6gxGyA9KVdv8KmmmPgtsjRW2zIABBah2Y1WNNV7JzkBAAEC',
        }

simple_replies_filename = 'simple_replies.json'
simple_replies = json.load(open(simple_replies_filename, 'r'))
def save_simple_replies():
    json_replies = json.dumps(simple_replies, indent='\t', sort_keys=True, ensure_ascii=False)
    with open(simple_replies_filename, 'w') as f:
        f.write(json_replies)
        f.write('\n')

save_simple_replies()

admin_ids = [
        414604698
        ]

module_list = {}
module_list.update(json.load(open('sem1moduleList.json', 'r')))
module_list.update(json.load(open('sem2moduleList.json', 'r')))

wikiwiki = wikipediaapi.Wikipedia('en')

def is_substr(x, y):
    return y.find(x) != -1

def is_subseq(x, y):
    x = x.split()
    y = y.split()
    it = iter(y)
    for wordx in x:
        for wordy in it:
            if is_substr(wordx, wordy):
                break
        else:
            return False
    return True

def randomcmd(bot, update):
    update.message.reply_text('{0:.3f}'.format(random.random()))

def hoogle(bot, update):
    update.message.reply_text("Hoogle doesn't work on this server... :(")
    # query = update.message.text[len('/hoogle'):]
    # result = subprocess.check_output(['hoogle', '--', query]).decode('utf-8')
    # update.message.reply_text(result)

def mancmd(bot, update):
    query = update.message.text.split()[1]
    result = subprocess.run(['man', '--', query], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode('utf-8').splitlines()
    if len(result) == 1:
        update.message.reply_text(result[0])
    else:
        name = -1
        description = -1
        reply = ""
        for i, l in enumerate(result):
            if l == 'NAME':
                name = i
            elif l == 'DESCRIPTION':
                description = i
        if name >= 0:
            reply += 'NAME: '
            reply += result[name+1].strip()
            reply += '\n'
        if description >= 0:
            reply += 'DESCRIPTION: '
            reply += result[description+1].strip()
            reply += '\n'
        if reply == "":
            reply += "Man page exists but someone fucked up when writing the manpage so... sorry :("
        update.message.reply_text(reply)

def mce(bot, update):
    update.message.reply_photo(photos["metacircular"])

def shutupandleave(bot, update):
    bot.leave_chat(update.message.chat_id)

def photocmd(bot, update):
    print(update)

def addcmd(bot, update):
    if update.message.from_user.id in admin_ids:
        _, cmdname, reply = update.message.text.split(maxsplit=2)
        simple_replies[cmdname] = reply
        save_simple_replies()
    else:
        print(update)

def rmcmd(bot, update):
    if update.message.from_user.id in admin_ids:
        _, cmdname, *_ = update.message.text.split(maxsplit=2)
        del simple_replies[cmdname]
        save_simple_replies()
    else:
        print(update)

def evaluatescheme(bot, update):
    _, code = update.message.text.split(maxsplit=1)
    # code = sexpr.parse(code)
    print(code)

def wiki(bot, update):
    _, query = update.message.text.split(maxsplit=1)
    page = wikiwiki.page(query)
    update.message.reply_text(f'''{page.fullurl}''')

def wikipedia(bot, update):
    _, query = update.message.text.split(maxsplit=1)
    page = wikiwiki.page(query)
    update.message.reply_text(f'''{page.summary}

{page.fullurl}''')

def nusmods(bot, update):
    _, query, *rest = update.message.text.split()
    if query.upper() in module_list:
        update.message.reply_markdown(get_mod_info(query, *rest))
    _, query = update.message.text.split(maxsplit=1)
    query = query.strip()
    matches = []
    for modcode, modname in module_list.items():
        if is_subseq(query.lower(), modname.lower()):
            matches.append((modcode, modname))

    if len(matches) == 0:
        update.message.reply_markdown('No matches found')
    elif len(matches) == 1:
        update.message.reply_markdown(get_mod_info(matches[0][0]))
    elif len(matches) > 10:
        update.message.reply_markdown('\n'.join([
            '''Top 10 matches found:''',
            *(f'''{x[0]}: {x[1]}''' for x in matches[:10]),
            '...']))
    else:
        update.message.reply_markdown('\n'.join([
            '''Matches found:''',
            *(f'''{x[0]}: {x[1]}''' for x in matches)]))

def get_mod_info(module_code, *options):
    r = requests.get(f'http://api.nusmods.com/2018-2019/modules/{module_code.upper()}/index.json')
    modinfo = r.json()

    newline = '\n'

    moddesc = modinfo.get('ModuleDescription', '').strip()
    semesters = [x.get('Semester', 0) for x in modinfo.get('History', [])]
    hasexam = any('ExamDate' in x for x in modinfo.get('History', []))

    title = f'''*{modinfo.get('ModuleCode', module_code.upper()).strip()} {modinfo.get('ModuleTitle', '').strip()}*'''
    mc = f'({modinfo["ModuleCredit"]} MC)''' if 'ModuleCredit' in modinfo else ''
    sems = ' ∙ '.join(f'Sem {x}' for x in semesters)

    examtimes = '\n'.join(
            f'''Sem {x['Semester']}: ''' + (
                f'''{datetime.datetime.strptime(x['ExamDate'], '%Y-%m-%dT%H:%M+0800').strftime('%d %b %Y %H:%M')}'''
                if 'ExamDate' in x
                else 'No Exam')
            for x in modinfo.get('History', []))

    header = f'''{title} {mc}'''.strip()

    if not options and 'exam' not in options:
        header += '\n'
        header += f'''{sems} {'' if hasexam else '-- *No exam*'}'''.strip()
        header += '\n'

    data = {
        'short': min(
            moddesc[:moddesc.find('. ')] + '.',
            moddesc[:moddesc.find('! ')] + '!',
            moddesc[:moddesc.find('? ')] + '?'),

        'desc': f'''
*Description*
{moddesc}
            '''.rstrip(),

        'prereq': f'''
*Prerequisites*
{modinfo.get('Prerequisite', 'Nil').strip()}
            '''.rstrip(),

        'exam': f'''
*Exam*
{examtimes}
            '''.rstrip(),
    }

    smalldata = {
        'short': min(
            moddesc[:moddesc.find('. ')] + '.',
            moddesc[:moddesc.find('! ')] + '!',
            moddesc[:moddesc.find('? ')] + '?'),
        'desc': moddesc,
        'prereq': modinfo.get('Prerequisite', 'Nil').strip(),
        'exam': examtimes,
    }

    options = options or ['short', 'prereq']
    content = '\n'.join(data[x] for x in options)

    if len(options) == 1:
        return f'''
{header}
{smalldata[options[0]]}
            '''.strip()
    else:
        return f'''
{header}
{content}
            '''.strip()

def xkcd(bot, update):
    _, query = update.message.text.split(maxsplit=1)
    update.message.reply_text(f'https://www.xkcd.com/{query}/')

modifiers = {
        'random': lambda s: ''.join(x.lower() if random.random() < 0.5 else x.upper() for x in s),
        'delete': lambda s: ''.join(x for x in s if random.random() < 0.8),
        'upper': lambda s: s.upper(),
        'lower': lambda s: s.lower(),
        'title': lambda s: s.title(),
        'expand': lambda s: ' '.join(s),
        'code': lambda s: f'```\n{s}\n```',
        'expand': lambda s: ' '.join(s),
        'smallcaps': lambda s: s.translate(str.maketrans("abcdefghijklmnopqrstuvwxyz","ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴩǫʀꜱᴛᴜᴠᴡxʏᴢ")),
        'wide': lambda s: s.translate(str.maketrans('!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~ ', '！＂＃＄％＆＇（）＊＋，－．／０１２３４５６７８９：；＜＝＞？＠ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ［＼］＾_｀ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ｛｜｝～　')),
        }

def simple(bot, update):
    command, *modifier = update.message.text.split()
    command = command.split('@', maxsplit=1)[0]
    command = command[1:]
    if command in simple_replies:
        text = simple_replies[command]
        for mod in modifier:
            if mod in modifiers:
                text = modifiers[mod](text)
        print(text)
        update.message.reply_markdown(text)

def main():
    updater = Updater('723571546:AAEPw61TLAhXYbVuOQgfsUScGrxFLNa2s0I')
    updater.dispatcher.add_handler(CommandHandler('random', randomcmd))
    updater.dispatcher.add_handler(CommandHandler('hoogle', hoogle))
    updater.dispatcher.add_handler(CommandHandler('man', mancmd))
    updater.dispatcher.add_handler(CommandHandler('mce', mce))
    updater.dispatcher.add_handler(CommandHandler('addcmd', addcmd))
    updater.dispatcher.add_handler(CommandHandler('rmcmd', rmcmd))
    updater.dispatcher.add_handler(CommandHandler('shutupandleave', shutupandleave))
    # updater.dispatcher.add_handler(CommandHandler('eval', evaluatescheme))
    updater.dispatcher.add_handler(CommandHandler('wiki', wiki))
    updater.dispatcher.add_handler(CommandHandler('wikipedia', wikipedia))
    updater.dispatcher.add_handler(CommandHandler('mod', nusmods))
    updater.dispatcher.add_handler(CommandHandler('xkcd', xkcd))

    updater.dispatcher.add_handler(MessageHandler(Filters.photo, photocmd))

    updater.dispatcher.add_handler(MessageHandler(Filters.command, simple))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
