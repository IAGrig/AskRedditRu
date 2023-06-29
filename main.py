import image_creator
import scraper
import translator
import config
import file_manager
import time

start_time = time.time()

post_id = input("Enter id:")

title, comments = scraper.get_post_json(post_id, config.COUNT_OF_POSTS)

translated_title = translator.translate_en2ru(title)
translated_comments = translator.translate_list(comments)



# TODO connect with telegram
# TODO connect with VK

print(translated_title)

for index in range(len(translated_comments)):
    print(f'{index} {translated_comments[index]}')

good_indexes = list(map(int, input('Specify indexes with comma:').split(',')))

post_comments = [translated_comments[index] for index in good_indexes]

file_manager.clean_folder('./images')

image_creator.generate_images(translated_title, post_comments)

print(time.time() - start_time, 'seconds')
file_manager.open_explorer_on('./images/title.jpg')

# telegram
# vk
