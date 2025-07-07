from openai import AsyncOpenAI
from collections import defaultdict
import config
user_conversations = defaultdict(list)

# Get a token on the website https://openrouter.ai/
AI_TOKEN = config.deepseek_token

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=AI_TOKEN,
)


# The function of sending a user's request to the ChatGPT
async def deepseek_generate(user_id: int, text: str, clear_history: bool = False):
    # If the history is cleared
    if clear_history:
        user_conversations[user_id] = []
        return "The dialog history has been cleared."

    # PopitusGPT memory
    user_conversations[user_id].append({"role": "user", "content": text})

    # If the user has sent more than 10 messages, the bot's memory is cleared
    if len(user_conversations[user_id]) > 10:
        user_conversations[user_id] = user_conversations[user_id][-10:]

    # Sending a user's request to ChatGPT
    try:
        completion = await client.chat.completions.create(
            model="deepseek/deepseek-chat:free",
            messages=user_conversations[user_id]
        )

        assistant_message = completion.choices[0].message.content
        user_conversations[user_id].append({"role": "assistant", "content": assistant_message})

        return assistant_message
    except Exception as e:
        return f"Error: {str(e)}"

