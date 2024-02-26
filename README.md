# Quizabot

Telegram bot to automatically answer trivia game Quizarium's questions

![Demo gif](.github/quizabot.gif)

## Method comparison

There are 3 methods you can use to find answers for the questions; below are the results of their performance in a test against 200 random questions:

| Method            | Accuracy | Average time taken |
| ----------------- | -------- | ------------------ |
| Google            | 82%      | 0.599s             |
| DuckDuckGo        | 71%      | 1.097s             |
| LLM (ChatDolphin) | 66%      | 4.128s             |

## Usage

Warning: Quizarium seems to have new anti-bot measures, proceed with caution and at your own risk!

1. Clone repo, install dependencies in requirements.txt
2. Rename template.env to .env
3. Obtain your [Telegram API ID and hash](https://docs.telethon.dev/en/stable/basic/signing-in.html)
4. (Optional) Create a [NLP Cloud](https://nlpcloud.com/) account and get your API key
5. Create a group chat with the Quizarium bot and copy the chat ID
6. Update `.env` with all above information
7. Run `main.py`

## License

[GNU General Public License v3.0](LICENSE)
