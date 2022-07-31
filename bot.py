from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
from PIL import Image



bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)
storage = MemoryStorage()
size = 512, 512
file = 'image.png'
@dp.message_handler(commands=['start','help'])
async def command_start(message : types.Message):
    await bot.send_message(message.from_user.id, 'You can upload any photo and automatically convert to 512x512 png for @Stickers bot')

@dp.message_handler(content_types=types.ContentTypes.PHOTO)
async def send_to_admin(message: types.Message):
    file_info = await bot.get_file(message.photo[-1].file_id)
#    await message.photo[-1].download(str(message.chat.id) + 'test.jpg') #deprecated
    await message.photo[-1].download(
        destination_file=str(message.chat.id) + 'test.jpg',
        )
    with Image.open(str(message.chat.id) + 'test.jpg') as im:
        im.thumbnail(size)
        im.save(str(message.chat.id) + file, "PNG")
    file_png = open(str(message.chat.id) + file, "rb")
    await bot.send_document(message.from_user.id, document=file_png)


@dp.message_handler()
async def echo_send(message : types.Message):
    #await message.answer(len(message.text))
    await bot.send_message(message.from_user.id, f'What do you mean about {message.text}? Are you OK? Please send a PHOTO!')
    print(len(message.text))
    #await message.reply(message.text)
    
    

executor.start_polling(dp, skip_updates=True)
