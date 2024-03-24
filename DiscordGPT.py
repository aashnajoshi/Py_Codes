# openai==0.28
import openai
import discord

openai.api_key = "YOUR_OPENAI_API_KEY"

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.author == self.user:  # Ignore messages from bot
            return
        if self.user in message.mentions:  # Check bot mention
            if any(word in message.content.lower() for word in ["hi", "hello", "hey", "greetings"]):
                await message.channel.send(f"Hello {message.author.mention}! I am a Work-In-Progress GPT Bot!")
            else:
                question = message.content.replace(f'<@!{self.user.id}>', '').strip()  # Remove bot mention
                response = self.ask_gpt(question)
                await message.channel.send(f"{message.author.mention}, {response}")

    def ask_gpt(self, question):
        prompt = f"Question: {question}\nAnswer:"
        response = openai.Completion.create(prompt=prompt, model="gpt-3.5-turbo-instruct", max_tokens=150,)
        return response.choices[0].text.strip()

intents = discord.Intents.default()
intents.messages = True
client = MyClient(intents=intents)
client.run('YOUR_DISCORD_BOT_TOKEN')