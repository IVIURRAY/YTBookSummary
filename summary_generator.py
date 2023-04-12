import os
import openai
from pathlib import Path
from dotenv import load_dotenv

from video_utils import get_video_id, get_video_url

if __name__ == '__main__':
    load_dotenv()
    book = input('What book summary would you like? ')
    speaker = input('What speaking style would you like to use? (e.g. cowboy, vampire) ')

    openai.api_key = os.getenv('OPEN_API_KEY')

    print("Generating structure...", end=" ")
    structure_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": (
                "You are a personal assistant who specialises in writing outlines for book summaries. You should "
                "respond with a JSON array of headings for a summary of the book requested. Answer as concisely as "
                'possible in the following format:\n["Heading 1", "Heading 2", ...]'
            )},
            {"role": "user", "content": f"Book: {book}"}
        ]
    )
    print("done!")

    structure_content = structure_response["choices"][0]["message"]['content']

    print("Generating summary...", end=" ")
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"You are a book summariser with 10 years experience. Answer in plain text only."},
            {"role": "user", "content": f"Write a summary of the book {book}, speaking in the style of a {speaker}. "
                                        f"Here is a JSON array of book summary headings: {structure_content}. "}
        ]
    )

    txt = response['choices'][0]['message']['content']
    summaries_dir = Path('summaries')
    summaries_dir.mkdir(parents=True, exist_ok=True)
    (summaries_dir / f"{book.replace(' ', '_')}_as_a_{speaker.replace(' ', '_')}.txt").write_text(txt)

    print("done!")

    video_id = get_video_id(txt)
    print(video_id)
    video_url = get_video_url(video_id)
    print(video_url)
