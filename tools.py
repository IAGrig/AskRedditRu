import scraper
import config
import translator
import json

def get_translated_tittle_and_posts(post_id: str) -> tuple[str, list]:
    title, comments = scraper.get_post_json(post_id, config.COUNT_OF_POSTS)
    translated_title = translator.translate_en2ru(title)
    translated_comments = translator.translate_list(comments)
    return translated_title, translated_comments

def write_tittle_and_comments_to_file(tittle: str, comments: list) -> None:
    json_dict = {"tittle":tittle, "comments":comments}
    with open(config.COMMENTS_FILE_PATH, 'w', encoding='utf-8') as file:
        json.dump(json_dict, file)

def get_tittle_and_posts_from_file() -> tuple[str, list]:
    with open(config.COMMENTS_FILE_PATH) as file:
        json_dict = json.load(file)

    return json_dict["tittle"], json_dict["comments"]
