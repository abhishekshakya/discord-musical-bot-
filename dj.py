import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os

client = commands.Bot(command_prefix='>',description="aaja baby aaja tera gana bja du")
client.remove_command('help')


station=705376208745005121
dj = 707218152307818507



@client.event
async def on_ready():
    print("Bot has started")



@client.command()
async def help(ctx):
    author = ctx.message.author

    embed = discord.Embed(
        colour = discord.Color.orange()
    )
    st = '''here are all the commands

    {use dot(>) as prefix before any command}

    **example**                  **description**

    >join                                   *for DJ to join channel*

    >dc                                     *for DJ to disconnect*

    >play *youtube-link*                 *to play song*

    >pause                                  *to pause*
    
    >resume                                 *to resume*      

    '''
    embed.set_author(name='help')
    embed.add_field(name="Hello There!!",value=st,inline=True)

    await ctx.send(st)

@client.command()#needed pynacl package for voice
async def join(ctx):
    channel = client.get_channel(station)
    ind=0
    mem = client.get_all_members()
    
    print(type(mem),mem)
    voice = get(client.voice_clients, guild = ctx.guild)
    mapp = channel.voice_states
    key = mapp.keys()
    for i in mapp:
        if i == dj and mapp[i].channel == channel:
            for i in mem:
                if i.id == dj:
                     await i.move_to(None)
            break
    voice = await channel.connect()
    await ctx.channel.send("connected")



@client.command()
async def dc(ctx):
    channel = client.get_channel(station)
    vc = client.voice_clients
    for i in vc:
        if i.channel.id == station:
            await i.disconnect()
            await ctx.channel.send(f"kr diya leave {channel}")
            return

    await ctx.channel.send("already dc hu")

@client.command()
async def play(ctx, url: str):
    song = os.path.isfile("song.mp3")
    try:
        if song:
            os.remove("song.mp3")
            print("Removed old song file")
    except PermissionError:
       
        print("Song is being played")
        await ctx.send("some song's playing already")
        await stop(ctx)
        os.remove("song.mp3")
        print("Removed old song file")
        
    
    await ctx.send("getting everything ready")
    voice = get(client.voice_clients,guild=ctx.guild)

    ydl_opts = {
        'format' : 'bestaudio/best',
        'postprocessors' : [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec':'mp3',
            'preferredquality':'192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio ...\n")
        ydl.download([url])
    
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            os.rename(file, "song.mp3")
    
    voice.play(discord.FFmpegPCMAudio("song.mp3"),after = lambda e: print(f"{name} has finished playing"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.8

    nname = name.rsplit("-",2)
    await ctx.send(f"playing: {nname}")



@client.command()
async def pause(ctx):

    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Music paused")
        voice.pause()
        await ctx.send("Music paused")
    else:
        print("Music not playing failed pause")
        await ctx.send("Music not playing failed pause")


@client.command()
async def resume(ctx):

    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        print("Resumed music")
        voice.resume()
        await ctx.send("Resumed music")
    else:
        print("Music is not paused")
        await ctx.send("Music is not paused")


@client.command()
async def stop(ctx):

    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Music stopped")
        voice.stop()
        await ctx.send("Music stopped")
    else:
        print("No music playing failed to stop")
        await ctx.send("No music playing failed to stop")


client.run(os.environ['token'])#for heruku)
