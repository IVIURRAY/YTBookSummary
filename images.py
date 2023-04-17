import base64
import os
import uuid
from pathlib import Path
from typing import Tuple

import httpx

PROMPT = (
    "a linkedin-style profile photograph of a {speaker}, facing the camera straight "
    "on, face central, neutral expression, Rembrandt lighting, photograph, single "
    "person, head fully visible, close crop"
)

async def create_profile_image(speaker: str) -> Tuple[Path, str]:
    """Create a profile image for a speaker using DreamStudio, return the path to the
    image and the base64 encoded image"""
    key = os.getenv("DREAMSTUDIO_API_KEY")
    if not key:
        raise ValueError("No API key found for DreamStudio")

    async with httpx.AsyncClient(timeout=httpx.Timeout(60, connect=60)) as client:
        response = await client.post(
            (
                "https://api.stability.ai/v1"
                "/generation/stable-diffusion-512-v2-1/text-to-image"
            ),
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {key}",
            },
            json={
                "text_prompts": [
                    {
                        "text": PROMPT.format(speaker=speaker),
                    },
                ],
                "cfg_scale": 1,
                "clip_guidance_preset": "FAST_BLUE",
                "height": 512,
                "width": 512,
                "samples": 1,
                "steps": 50,
            },
        )

        if response.status_code != 200:
            raise ValueError(response.text)

        image_path = Path("images") / f"{speaker}_{uuid.uuid4()}.png"
        image_base64 = response.json()["artifacts"]["base64"]
        image_path.write_bytes(base64.b64decode(image_base64))

    return image_path, image_base64


def main():
    import asyncio
    from dotenv import load_dotenv

    load_dotenv()
    asyncio.run(create_profile_image("cowboy"))


if __name__ == '__main__':
    main()
