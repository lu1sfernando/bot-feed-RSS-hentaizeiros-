import discord
import feedparser
import asyncio
from pypresence import Presence

# Configure os intents
intents = discord.Intents.default()
intents.messages = True  # Permite que o bot escute mensagens

TOKEN = 'MTI5ODc5ODA5OTE4NzM3MjEyMg.GyMBrr.x9gPTOVKJCIpOalN0O2OyP5ULdaNVpG7hO2u9o'  # Token de exemplo
CHANNEL_ID = 881337064388431872  # ID do canal onde o bot irá enviar as mensagens
rss_feeds = ['https://animeshentai.tv/episodios/feed/']  # URL do feed RSS
posted_links = set()  # Armazena links já postados
CHECK_INTERVAL = 300  # Intervalo de checagem em segundos

# IDs dos cargos a serem mencionados
ROLE_IDS = []

client = discord.Client(intents=intents)

async def check_rss_feed():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)

    # Obtém os cargos pelo ID
    roles = [channel.guild.get_role(role_id) for role_id in ROLE_IDS]

    while not client.is_closed():
        try:
            for feed_url in rss_feeds:
                print(f'Checando o feed RSS em {feed_url}...')  # Mensagem de log
                feed = feedparser.parse(feed_url)
                for entry in feed.entries:
                    if entry.link not in posted_links:
                        posted_links.add(entry.link)
                        # Menciona todos os cargos
                        mention = " ".join(role.mention for role in roles if role)  # Garante que o cargo exista
                        await channel.send(f"{mention} Novo episódio: {entry.title}\n{entry.link}") 
                        print(f'Postando novo episódio: {entry.title}')  # Mensagem de log
                        await asyncio.sleep(300)  # Pausa de 5 minutos (300 segundos)
            await asyncio.sleep(CHECK_INTERVAL)
        except Exception as e:
            print(f'Ocorreu um erro: {e}')
            await asyncio.sleep(5)  # Aguarda 5 segundos antes de tentar novamente

@client.event
async def on_ready():
    print(f'Bot conectado como {client.user}')

async def main():
    await client.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())










