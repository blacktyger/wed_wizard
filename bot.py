# :SAD:D

from aiogram import *
from aiogram.types import ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

from db import Database
from keys import TOKEN
from tools import icon_number, help_msg, Response, time, Link

# Initialize Database object
db = Database('wizard_test1')

# Telegram BOT Token
bot = Bot(token=TOKEN)

# aiogram stuff
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Future Keyboard
# button1 = KeyboardButton('Thanks')
# button2 = KeyboardButton('Bye!')
# markup3 = ReplyKeyboardMarkup().row(button1, button2)

# BOT SETTINGS
ADMINS = ['blacktyg3r']

COMMANDS = {'help': ['help', 'Help', 'HELP',
                     'start', 'Start', 'START'],
            'add': ['add', 'ADD', 'Ad'],
            'show': ['show', 'Show', 'SHOW'],
            'like': ['done', 'Done', 'DONE',
                     'like','Like', 'LIKE',
                     'tick', 'Tick', 'TICK'],
            'delete': ['remove', 'Remove', 'REMOVE'],
            'remove_all': ['REMOVE_ALL']}
short_time = 20
last_show_msg = 0
last_help_msg = 0


@dp.message_handler(commands=COMMANDS['help'])
async def help_command(message: types.Message):
    user = message.from_user
    db.add_user(user)
    reply = Response('🧙🏼‍♂', f"<b>@WednesdayWizardBot SPELL BOOK 📃</b>")
    reply.body.pop(-1)
    lines = help_msg()
    reply.lines = lines
    reply.add_lines()
    send = await message.reply(f'{reply.print()}', parse_mode=ParseMode.HTML, reply=False)
    global last_help_msg
    if last_help_msg:
        await bot.delete_message(message.chat.id, last_help_msg)
    last_help_msg = send.message_id
    await asyncio.sleep(short_time)
    await message.delete()
    await send.delete()


@dp.message_handler(commands=COMMANDS['add'])
async def add_command(message: types.Message):
    if message.is_command():
        url = message.get_args()
        user = message.from_user.username
        link = {'time': time(), 'url': url, 'author': user,
                'votes': 0, 'voters': [], 'msg_id': message.message_id}
        link = Link(**link)
        if db.add_link(link):
            reply = f" 🧙🏼‍♂ Great spell @{user}, magic link added!"
            send = await message.reply(f'{reply}', parse_mode=ParseMode.HTML, reply=False,
                                       disable_notification=True, disable_web_page_preview=False)
            await asyncio.sleep(short_time)
            await send.delete()
        else:
            reply = f" 🧙🏼‍♂ Oops @{user}, magic link already here!"
            send = await message.reply(f'{reply}', parse_mode=ParseMode.HTML, reply=False,
                                       disable_notification=True, disable_web_page_preview=False)
            await asyncio.sleep(short_time)
            await send.delete()


@dp.message_handler(commands=COMMANDS['show'])
async def show_command(message: types.Message):
    if message.is_command():
        if message.get_args() != '':
            length = int(message.get_args())
        else:
             length = 5
        reply = Response('🧙🏼‍♂', "MAGIC LINK LIST 🖇")
        lines = [f"LINK_ID: <b>{i}</b> | {link.time} | {icon_number(link.votes)} 👍\n{link.url}"
                 for i, link in enumerate(db.read()['links'])]
        lines.reverse()
        lines = lines[:length]
        reply.lines = lines
        reply.add_lines()
        print(db.read())
        send = await message.reply(f'{reply.print()}', parse_mode=ParseMode.HTML, reply=False,
                                   disable_notification=True, disable_web_page_preview=True)
        global last_show_msg
        if last_show_msg:
            await bot.delete_message(message.chat.id, last_show_msg)
        last_show_msg = send.message_id
        await asyncio.sleep(short_time)
        await message.delete()
        await send.delete()


@dp.message_handler(commands=COMMANDS['like'])
async def done_command(message: types.Message):
    if message.is_command():
        ids = message.get_args().split(' ')
        user = message.from_user.username
        for id in ids:
            print(id)
            link = db.get_links()[int(id)]
            if user not in link.voters:  # and user != link['author']:
                link.voters.append(user)
                link.votes += 1
                db.update_link(link)
                reply = f"🧙🏼‍♂ @{user} IS BLESSING LINK_ID: <b>{', '.join(ids)}</b> 🎊"
            else:
                reply = f"🧙🏼‍♂ @{user}, LINK_ID: <b>{', '.join(ids)}</b> ALREADY BLESSED!"

        send = await message.reply(f'{reply}', parse_mode=ParseMode.HTML, reply=False,
                                   disable_notification=True, disable_web_page_preview=True)
        await asyncio.sleep(int(short_time / 2))
        await message.delete()
        await send.delete()


@dp.message_handler(commands=COMMANDS['delete'])
async def delete_command(message: types.Message):
    if message.is_command():
        user = message.from_user.username
        ids = message.get_args().split(' ')
        for id in ids:
            link = db.get_links()[int(id)]
            if user == link.author or user in ADMINS:
                db.remove_link(link)
                print('REMOVED:', link)
                reply = f"🧙🏼‍♂ @{user} MADE LINK_ID: <b>{', '.join(ids)}</b> | DISAPPEAR! "
            else:
                reply = f"🧙🏼‍♂ @{user}, LINK_ID: <b>{', '.join(ids)}</b> IS NOT YOURS!"

        send = await message.reply(f'{reply}', parse_mode=ParseMode.HTML, reply=False,
                                   disable_notification=True, disable_web_page_preview=True)
        await asyncio.sleep(int(short_time / 2))
        await message.delete()
        await send.delete()


@dp.message_handler(commands=COMMANDS['remove_all'])
async def delete_all_command(message: types.Message):
    if message.is_command():
        user = message.from_user.username
        if user in ADMINS:
            db.remove_all_links()
            print('REMOVED ALL')
            reply = f'🧙🏼‍♂ @{user} ~~ AVADA KEDAVRA 🧬🦠  KILLED ALL LINKS!'
        else:
            reply = f"🧙🏼‍♂ @{user} IT'S DARK MAGIC, DON'T TRY!"

        send = await message.reply(f'{reply}', parse_mode=ParseMode.HTML, reply=False,
                                   disable_notification=True, disable_web_page_preview=True)
        await asyncio.sleep(short_time)
        await message.delete()
        await send.delete()


@dp.message_handler()
async def delete_all_command(message: types.Message):
    if message.is_command():
        if message.get_command() not in COMMANDS:
            if message.get_args() != "":
                await message.delete()


# START BOT
if __name__ == '__main__':
    print("starting")
    executor.start_polling(dp, skip_updates=True)