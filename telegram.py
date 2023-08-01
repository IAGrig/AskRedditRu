# TODO logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command, CommandObject 

import config
import tools
import file_manager
import image_creator

bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("AskRedditRu bot ia awailable\nType /askreddit <post id> to start work")

@dp.message(Command("askreddit"))
async def cmd_askreddit(message: types.Message, command: CommandObject):
    if command.args:
        try:
            tittle, comments = tools.get_translated_tittle_and_posts(command.args) 
            answer_message_text = tittle + "\n"
            for index in range(len(comments)):
                answer_message_text += str(index)+" "+comments[index]+"\n"

            tools.write_tittle_and_comments_to_file(tittle, comments)
            #  4096 because of Telegram limits
            for step in range((len(answer_message_text)+4095)//4096):
                await message.answer(answer_message_text[step*4096:(step+1)*4096])

            await message.answer("Choose comment numbers comma-separated that I should post to VK group")
        except Exception as e:
            print(e)
            await message.answer("Error. Try again or change post id")
            await message.answer(str(e))
        
    else:
        await message.answer("You should send me post id")


@dp.message(F.text)
async def handle_comment_numbers(message: types.Message):
    message_text = message.text
    message_text = str(message_text).replace(' ', '')
    post_comment_ids = list(map(int, message_text.split(',')))

    tittle, comments = tools.get_tittle_and_posts_from_file()

    post_comments = [comments[id] for id in range(len(comments)) if id in post_comment_ids]

    file_manager.clean_folder('./images')
    image_creator.generate_images(tittle, post_comments)

    await message.answer('Done! Files created.\nIf you want to post to VK group send me /vkpost')

@dp.message(Command("vkpost"))
async def cmd_vkpost(message: types.Message):
    pass




# TODO config modification: comments file path, font file
    


async def tg_main():
    await dp.start_polling(bot)

