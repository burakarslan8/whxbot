import discord
import asyncio
import json
import openai

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
model_id = "gpt-3.5-turbo-0613"

with open('config.json') as f:
    config = json.load(f)
    openai.api_key = config['ai-api-key']
    bot_token = config['bot-token']
    context = config['context']

conversation_history = [{"role": "system", "content": context}]

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    activity = discord.Game(name="I'm here to chat. Use !whx to say hi!")
    await client.change_presence(activity=activity)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('!whx'):
        question = message.content[5:]

        conversation_history.append({"role": "user", "content": question})

        response = call_chatgpt_api(conversation_history)

        await message.channel.send(response)

def call_chatgpt_api(question):
    try:
        response = openai.ChatCompletion.create(
            model=model_id,
            messages= conversation_history
        )

        conversation_history.append({"role": "assistant", "content": response.choices[0].message['content']})

        return response.choices[0].message['content']
    
    except Exception as e:
        return f"An error occurred: {str(e)}"

client.run(bot_token)