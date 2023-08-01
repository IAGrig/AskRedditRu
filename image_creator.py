from PIL import Image, ImageDraw, ImageFont
import config

FILENAME = config.BACKGROUND_IMAGE_PATH
START_X, START_Y = 60, 50

# fontsize : (num_of_rows, chars_per_row, summary_char_capability)
fontsizes = {20: (28, 54, 1512),
             25: (22, 43, 946),
             30: (18, 36, 648),
             35: (16, 31, 496),
             40: (14, 30, 420)}


def cut_comment(text: str):
    if len(text) > fontsizes[min(fontsizes.keys())][2]: return -1  # too large text
    fontsize = 40
    while len(text) > fontsizes[fontsize][2]: fontsize -= 5
    char_per_row = fontsizes[fontsize][1]
    chunks = []
    for ind in range(len(text) // char_per_row):
        chunks.append(text[char_per_row * ind:char_per_row * (ind + 1)])
    return chunks, fontsize


def cut_comment2(text: str):
    if len(text) > fontsizes[min(fontsizes.keys())][2]: return -1  # too large text
    fontsize = 40
    while len(text) > fontsizes[fontsize][2]: fontsize -= 5
    char_per_row = fontsizes[fontsize][1]
    chunks = []
    s = '  '
    count = 2
    text = text.replace('\n' * 5, '\n' * 4).replace('\n' * 4, '\n' * 3).replace('\n' * 3, '\n' * 2).replace('\n\n',
                                                                                                            '\n  ')
    for word in text.split(' '):
        if s == '  ':
            s = word
            count = len(word)
            continue

        if count + 1 + len(word) <= char_per_row:
            count += 1 + len(word)
            s += ' ' + word
        else:
            chunks.append(s)
            s = word
            count = len(word)
    chunks.append(s)

    return chunks, fontsize


def generate_image(text: str, filename: str = "filename") -> None:
    chunks, fontsize = cut_comment2(text) #  TODO raise exceptions and logging
    with Image.open(FILENAME) as image:
        image.load()
    font = ImageFont.truetype(config.FONT_PATH, fontsize)
    image_draw = ImageDraw.Draw(image)
    image_draw.multiline_text((START_X, START_Y), "\n".join(chunks), fill=(0, 0, 0), font=font)

    # image.show()
    image.save(f"./images/{filename}.jpg")


def generate_images(title: str, comments: list) -> None:
    generate_image(title, '00title')
    for index in range(len(comments)):
        generate_image(comments[index], str(index))

