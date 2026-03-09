import asyncio
import uuid
import edge_tts


async def generate_voice(text, voice):

    filename = f"speech_{uuid.uuid4().hex}.mp3"

    communicate = edge_tts.Communicate(text, voice)

    await communicate.save(filename)

    return filename


def speak(text, agent):

    if agent == "pro":
        voice = "en-US-JennyNeural"        # Female

    elif agent == "con":
        voice = "en-US-GuyNeural"          # Male

    elif agent == "judge":
        voice = "en-US-AriaNeural"         # Mature female

    else:
        voice = "en-US-JennyNeural"

    audio = asyncio.run(generate_voice(text, voice))

    return audio