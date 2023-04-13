import os
from distutils.util import strtobool

import openai
from pathlib import Path
from dotenv import load_dotenv

from video_utils import get_video_id, get_video_url


def write_txt_to_file(txt: str, book: str, speaker: str):
    summaries_dir = Path("summaries")
    summaries_dir.mkdir(parents=True, exist_ok=True)
    (
        summaries_dir / f"{book.replace(' ', '_')}_as_a_{speaker.replace(' ', '_')}.txt"
    ).write_text(txt)


def generate_book_structure(book: str) -> str:
    print("Generating structure...", end=" ")
    structure_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a personal assistant who specialises in writing outlines for book summaries. You should "
                    "respond with a JSON array of headings for a summary of the book requested. Answer as concisely as "
                    'possible in the following format:\n["Heading 1", "Heading 2", ...]'
                ),
            },
            {"role": "user", "content": f"Book: {book}"},
        ],
    )
    print("done!")

    return structure_response["choices"][0]["message"]["content"]


def generate_book_summary(structure_content: str, book: str, speaker: str) -> str:
    print("Generating summary...", end=" ")
    response = openai.ChatCompletion.create(
        model="gpt-4"
        if strtobool(os.getenv("USE_GPT_4", "false"))
        else "gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": f"You are a book summariser with 10 years experience. Answer in plain text only.",
            },
            {
                "role": "user",
                "content": f"Write a summary of the book {book}, speaking in the style of a {speaker}. "
                f"Here is a JSON array of book summary headings: {structure_content}. ",
            },
        ],
    )
    txt = response["choices"][0]["message"]["content"]
    print("done!")

    return txt


if __name__ == "__main__":
    load_dotenv()
    openai.api_key = os.getenv("OPEN_API_KEY")

    book = input("What book summary would you like? ")
    speaker = input(
        "What speaking style would you like to use? (e.g. cowboy, vampire) "
    )

    # Generate book summary
    structure = generate_book_structure(book)
    txt = generate_book_summary(structure, book, speaker)
    write_txt_to_file(txt, book, speaker)

    # Generate video
    video_id = get_video_id(txt)
    print(video_id)
    video_url = get_video_url(video_id)
    print(video_url)
