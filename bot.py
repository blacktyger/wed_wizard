from aiogram import *
from aiogram.types import ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from keys import TOKEN
from tools import icon_number, Response, time, Database, Link

# Initialize Database object
db = Database('wizard_test')

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
COMMANDS = ['help', 'add', 'remove', 'delete', 'del',
            'done', 'tick', 'liked', 'REMOVE_ALL']
short_time = 20
last_show_msg = 0


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    reply = Response('🧙🏼‍♂', "WednesdayWizard! 💬")
    lines = [
        "In order to add magic links type:",
        f"<code> /add [here goes magic link]</code>",
        f"The real magic starts with spell:",
        f"<code> /show [number of links, default 5]</code>",
        f"Please let us know you liked the link:",
        f"<code> /done [ID, ID2, etc]</code>",
        f"Other spells:",
        f"<code> /delete [ID]</code>",
        reply.separator
        ]
    reply.lines = lines
    reply.add_lines()
    send = await message.reply(f'{reply.print()}', parse_mode=ParseMode.HTML, reply=False)
    await asyncio.sleep(short_time * 2)
    await send.delete()
    await message.delete()


@dp.message_handler(commands=['add'])
async def add_command(message: types.Message):
    if message.is_command():
        url = message.get_args()
        user = message.from_user.username
        link = {'time': time(), 'url': url, 'author': user,
                'votes': 0, 'voters': [], 'msg_id': message.message_id}
        link = Link(**link)
        if db.add('links', link):
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


@dp.message_handler(commands=['show'])
async def show_command(message: types.Message):
    if message.is_command():
        length = message.get_args() or 5
        reply = Response('🧙🏼‍♂', "MAGIC LINK LIST 🖇")
        lines = [f"ID: <b>{i}</b> | {link.time} | {icon_number(link.votes)} 👍\n{link.url}"
                 for i, link in enumerate(db.get()['links'])][:length]
        reply.lines = lines
        reply.add_lines()
        print(db.get())
        send = await message.reply(f'{reply.print()}', parse_mode=ParseMode.HTML, reply=False,
                                   disable_notification=True, disable_web_page_preview=True)
        global last_show_msg
        if last_show_msg:
            try:
                await bot.delete_message(message.chat.id, last_show_msg)
            except:
                pass

        last_show_msg = send.message_id
        await asyncio.sleep(short_time)
        await message.delete()
        await asyncio.sleep(short_time)
        try:
            await send.delete()
        except:
            pass


@dp.message_handler(commands=['done', 'liked', 'tick'])
async def done_command(message: types.Message):
    if message.is_command():
        ids = message.get_args().split(' ')
        user = message.from_user.username
        for id in ids:
            link = db.get_links()[int(id)]
            if user not in link.voters:  # and user != link['author']:
                link.voters.append(user)
                link.votes += 1
                db.update_link(link)
                reply = f"🧙🏼‍♂ @{user} IS BLESSING LINK ID: <b>{', '.join(ids)}</b> 🎊"
            else:
                reply = f"🧙🏼‍♂ @{user}, LINK ID: <b>{', '.join(ids)}</b> ALREADY BLESSED!"

            send = await message.reply(f'{reply}', parse_mode=ParseMode.HTML, reply=False,
                                       disable_notification=True, disable_web_page_preview=True)
            await asyncio.sleep(int(short_time / 2))
            await message.delete()
            await send.delete()


@dp.message_handler(commands=['delete', 'remove', 'del'])
async def delete_command(message: types.Message):
    if message.is_command():
        user = message.from_user.username
        ids = message.get_args().split(' ')
        for id in ids:
            link = db.get_links()[int(id)]
            if user == link.author or user in ADMINS:
                db.remove_link(link)
                print('REMOVED:', link)
                reply = f"🧙🏼‍♂ @{user} MADE LINK ID: <b>{', '.join(ids)}</b> | DISAPPEAR! "
            else:
                reply = f"🧙🏼‍♂ @{user}, LINK ID: <b>{', '.join(ids)}</b> IS NOT YOURS!"

        send = await message.reply(f'{reply}', parse_mode=ParseMode.HTML, reply=False,
                                   disable_notification=True, disable_web_page_preview=True)
        await asyncio.sleep(int(short_time / 2))
        await message.delete()
        await send.delete()


@dp.message_handler(commands=['REMOVE_ALL'])
async def delete_all_command(message: types.Message):
    if message.is_command():
        user = message.from_user.username
        if user in ADMINS:
            db.remove_all()
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
            await message.delete()


# START BOT
if __name__ == '__main__':
    print("starting")
    executor.start_polling(dp, skip_updates=True)
