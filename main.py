import uvloop
uvloop.install()  # nopep8
import os
import helper
from pyrogram import Client, filters, types, idle, enums
from dotenv import load_dotenv

load_dotenv()

app = Client(os.getenv("BOT_NAME"),
             bot_token=os.getenv("BOT_TOKEN"),
             api_id=os.getenv("API_ID"), api_hash=os.getenv("API_HASH"))


# /start command
@app.on_message(filters.command("start"))
async def start(_, message: types.Message):
    """
    This function is the handler for the "/start" command.
    It sends a reply message to the user introducing the bot and its capabilities.

    Parameters:
        _: The unused parameter representing the client.
        message (types.Message): The message object representing the user's message.

    Returns:
        None
    """
    await message.reply("Hello! I'm a bot that can help you to summarize your voice messages. Just send me a voice message and I'll summarize it for you.\n\nif you want more information, send /help command\n\nMade with ❤️ by [FS-17](https: // github.com/FS-17)")


# if user send /convert command
@app.on_message(filters.command("convert") | filters.command("c"))
async def convert(_, message: types.Message):
    """
    Converts a voice message to text, when the user replies to a voice message.

    Args:
        _: The unused parameter representing the client.
        message (types.Message): The message object.

    Returns:
        None

    """

    if message.voice or message.audio:
        voice = message
    elif message.reply_to_message and (message.reply_to_message.voice or message.reply_to_message.audio):
        voice = message.reply_to_message
    else:
        await message.reply("Reply to a voice message or a voice note.", parse_mode=enums.ParseMode.MARKDOWN)
        return

    mid = await message.reply("Converting the voice message to text...", parse_mode=enums.ParseMode.MARKDOWN)

    # download the voice message
    file = await voice.download()
    texts = helper.speech_to_text(file)

    os.remove(file)
    mid.text = ""

    # combine the text
    for text in texts:
        try:
            mid.text = mid.text + text.text
            await mid.edit(mid.text, parse_mode=enums.ParseMode.MARKDOWN)
        except Exception as e:
            print(e)
            print(text.candidates)


# if user sends a voice or audio
@app.on_message(filters.command("summarize") | filters.command("s") | filters.audio | filters.voice)
async def summarize(_, message: types.Message):
    """
    This function is used to summarize a voice message.

    Args:
        _: The first argument is ignored.
        message (types.Message): The message object containing the voice message.

    Returns:
        None

    """

    # if user reply to a voice message
    if message.voice or message.audio:
        voice = message
    elif message.reply_to_message and (message.reply_to_message.voice or message.reply_to_message.audio):
        voice = message.reply_to_message
    else:
        await message.reply("Reply to a voice message or a voice note.", parse_mode=enums.ParseMode.MARKDOWN)
        return

    mid = await message.reply("Summarizing the voice message...", parse_mode=enums.ParseMode.MARKDOWN)

    # download the voice message
    path = await voice.download()

    mid.text = ""

    # get the summary
    texts = helper.summarize(path)
    os.remove(path)

    # combine the text
    for text in texts:

        try:
            mid.text = mid.text + text.text
            await mid.edit(f"{mid.text}", parse_mode=enums.ParseMode.MARKDOWN)

        except Exception as e:
            print(e)
            print(text.candidates)

    await message.reply("You can do more with this voice message:\n /help to see the commands", parse_mode=enums.ParseMode.MARKDOWN)


@app.on_message(filters.command("cut"))
async def cut(_, message: types.Message):
    """
    This function is used to cut the silence from a voice message.

    Args:
        _: The first argument is ignored.
        message (types.Message): The message object containing the voice message.

    Returns:
        None

    """

    # if user reply to a voice message
    if message.voice or message.audio:
        voice = message
    elif message.reply_to_message and (message.reply_to_message.voice or message.reply_to_message.audio):
        voice = message.reply_to_message
    else:
        await message.reply("Reply to a voice message or a voice note.", parse_mode=enums.ParseMode.MARKDOWN)
        return

    mid = await message.reply("Cutting the silence from the voice message...", parse_mode=enums.ParseMode.MARKDOWN)

    # download the voice message
    path = await voice.download()

    mid.text = ""

    # cut the silence
    newpath, duration = helper.cut_silence(path)

    # send to user the new voice message
    await message.reply_audio(newpath, title=f"duration: {duration}", duration=duration, parse_mode=enums.ParseMode.MARKDOWN)
    os.remove(path)
    os.remove(newpath)


@ app.on_message(filters.command("help"))
async def help(_, message: types.Message):
    await message.reply("the bot can make 3 things: \n1. summarize the voice message with /summarize command\n2. convert the voice message to text with /convert command\n3. cut the silence from the voice message with /cut command\n\nMade with ❤️ by[FS-17](github.com/FS-17)")


# echo for testing
@ app.on_message()
async def echo(_, message: types.Message):
    print(message.text)
    await message.reply(message.text)


if __name__ == "__main__":
    app.start()
    print("Bot is running!")
    idle()
    app.stop()
