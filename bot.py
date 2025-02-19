from http import client
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord import utils
import config
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('Бот запущен')


@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id == config.POST_ID:
        channel = bot.get_channel(payload.channel_id) # получаем объект канала
        message = await channel.fetch_message(payload.message_id) # получаем объект сообщения
        member = payload.member
 
        try:
            emoji = payload.emoji.name
            roleId = config.ROLES[emoji]
            role = message.guild.get_role(roleId)

            await member.add_roles(role)
            print('[SUCCESS] User {0.display_name} has been granted with role {1.name}'.format(member, role))
           
        except KeyError as e:
            print('[ERROR] KeyError, no role found for ' + emoji)
        except Exception as e:
            print(repr(e))
@bot.event
async def on_raw_reaction_remove(payload):
    print(payload)
    channel = await bot.fetch_channel(745758145640661095)
    message = await channel.fetch_message(payload.message_id) # получаем объект сообщения

    try:
        emoji = payload.emoji.name
        roleId = config.ROLES[emoji]
        role = message.guild.get_role(roleId)
 
        for member in bot.get_all_members():
            print(member)
            if member.id == payload.user_id:
                await member.remove_roles(role)
                print('[SUCCESS] Role {1.name} has been remove for user {0.display_name}'.format(member, role))
 
    except KeyError as e:
        print('[ERROR] KeyError, no role found for ' + emoji)
    except Exception as e:
        print(repr(e))
@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name = "Гость")
    await member.add_roles(role)
    wellcomechannel = bot.get_channel(940248018807054336)
    await wellcomechannel.send(f'Добро пожаловать, {member.mention}, в гильдию OneH1ve')
    
token = os.environ.get('BOT_TOKEN')
bot.run(token)
