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

@dp.message(Command("edit_tittle"))
async def cmd_edit_tittle(message: types.Message, command: CommandObject):
    if command.args:
        new_tittle = command.args
        tools.set_new_tittle_text(new_tittle)
        await message.answer("Done! If you want regenerate images just choose their numbers again. Tittle image will regenerate together with them")
    else:
        tittle, comment = tools.get_tittle_and_posts_from_file()
        await message.answer(tittle)
        await message.answer("You should send me new tittle.\n/edit_tittle <new tittle>")



@dp.message(Command("edit_comment"))
async def cmd_edit_comment(message: types.Message, command: CommandObject):
    if command.args:
        command_args_splitted = command.args.split()
        comment_id, new_comment_text = command_args_splitted[0], command_args_splitted[1:]
        if not new_comment_text and comment_id.isdecimal():
            comment_text = tools.get_comment_text_by_id(int(comment_id))
            await message.answer(comment_text)
        elif new_comment_text and comment_id.isdecimal():
            tools.set_new_comment_text(int(comment_id), " ".join(new_comment_text))
            await message.answer("Done! If you want regenerate images just choose their numbers again.")
        else:
            await message.answer("Incorrect input")

    else:
        await message.answer("You should send me comment id.\n/edit_comment <comment id>\nOR\n/edit_comment <comment id> <new comment text>")

@dp.message(Command("vkpost"))
async def cmd_vkpost(message: types.Message):
    pass


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


# TODO config modification: comments file path, font file
    

async def tg_main():
    await dp.start_polling(bot)

