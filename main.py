from summary_generator import (
    generate_book_structure,
    generate_book_summary,
    write_txt_to_file,
)
from upload_video import upload
from video_utils import get_video_id, get_video_url

if __name__ == "__main__":
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

    # Publish Video
    upload(
        "/Users/haydn/Downloads/noelle.mp4",
        f"Summary of {book} in the style of {speaker}",
        f"Here is a summary of the book {book}, in the speaker style of {speaker}! (Like, Subscribe and Comment)",
        f"{book},{speaker},book,summary",
        "22",  # See "https://developers.google.com/youtube/v3/docs/videoCategories/list"
        "private",
    )