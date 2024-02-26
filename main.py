import os
import re
from dotenv import load_dotenv
from sqlitedict import SqliteDict
from telethon import TelegramClient, events, errors

load_dotenv()

# answering methods
import search
import llm

QUIZARIUM_USER_ID = 155670507
TELEGRAM_API_ID = int(os.environ["TELEGRAM_API_ID"])
TELEGRAM_API_HASH = os.environ["TELEGRAM_API_HASH"]
CHAT_ID = int(os.environ["CHAT_ID"])
CACHE_PATH = os.environ["CACHE_PATH"]
ANSWER_SOURCE = os.environ["ANSWER_SOURCE"]

client = TelegramClient("user", TELEGRAM_API_ID, TELEGRAM_API_HASH)
cache = SqliteDict(CACHE_PATH, autocommit=True)

# globals
curr_question = None
curr_response = None
incorrect_answer = False


@client.on(events.NewMessage(chats=CHAT_ID, from_users=QUIZARIUM_USER_ID))
async def my_event_handler(event):
    global curr_question
    global curr_response
    global incorrect_answer

    # handle bot questions
    if "What is the name of this bot" in event.raw_text:
        await event.respond("Quizarium")

    elif "▶️ QUESTION" in event.raw_text:
        curr_question = event.raw_text.split("\n")[1]
        incorrect_answer = False  # reset whether current answer is correct
        print(f"New question: {curr_question}")

        # firstly, check if answer is already known
        if curr_question in cache:
            print("- Answering from cache")
            answer = cache[curr_question]

        # otherwise, obtain it by some specified method
        elif ANSWER_SOURCE == "search":
            print("- Answering from search")
            answer = search.get_answer(curr_question)

        elif ANSWER_SOURCE == "llm":
            print("- Answering from LLM")
            answer = llm.get_answer(curr_question)

        curr_response = await event.respond(answer)  # save message id for later edit

    # handle bot responses
    if curr_question is None or curr_response is None:
        # don't do anything if no current question or response is saved
        # i.e. the bot was started only after a question was asked
        return

    elif "✅ Yes" in event.raw_text:  # correct answer
        match = re.search("✅ Yes, ([\w ]+)!", event.raw_text)
        if not match:
            return

        print("- Correct answer; saving in cache")

        cache[curr_question] = match[1]
        await client.edit_message(curr_response, match[1])

    elif "Hint: " in event.raw_text and incorrect_answer == False:
        print("- Incorrect answer")

        await client.edit_message(curr_response, "hmm...")

        # since multiple hints are dropped, this prevents multiple edits / double couting
        incorrect_answer = True

    elif "⛔️ Nobody guessed" in event.raw_text:
        match = re.search("The correct answer was ([\w ]+)$", event.raw_text)
        if not match:
            return

        print("- Answer revealed; saving in cache")

        cache[curr_question] = match[1]
        await client.edit_message(curr_response, match[1])


client.start()
client.run_until_disconnected()
