from pyrogram import filters, Client
from AnonX import app
import asyncio
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from AnonX.core.call import Anon
from AnonX.utils.database import *
from pytgcalls.exceptions import (NoActiveGroupCall,TelegramServerError)

@app.on_message(filters.regex("منو بالمكالمه"))
async def strcall(client, message):
    assistant = await group_assistant(Anon,message.chat.id)
    try:
        await assistant.join_group_call(message.chat.id, AudioPiped("./assets/vega.mp3"), stream_type=StreamType().pulse_stream)
        text="🔔 الاعضاء المتواجدين في المكالمه :\n\n"
        participants = await assistant.get_participants(message.chat.id)
        k =0
        for participant in participants:
            info = participant
            if info.muted == False:
                mut="**يحجي**"
            else:
                mut="**ساكت**"
            user = await client.get_users(participant.user_id)
            k +=1
            text +=f"{k}➤{user.mention}➤{mut}\n"
        text += f"\nعددهم : {len(participants)}\n✔️"    
        await message.reply(f"{text}")
        await asyncio.sleep(5)
        await assistant.leave_group_call(message.chat.id)
    except NoActiveGroupCall:
        await message.reply(f"عمو المكالمه اصلا مسدوده**\n")
    except TelegramServerError:
        await message.reply(f"ارسل الامر ثاني في مشكله في سيرفر التلجرام\n")
        
        
