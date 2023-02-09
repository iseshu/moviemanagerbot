import asyncio
import httpx
import re
from helper import *
from pyrogram import filters, Client,enums
from pyrogram.types.messages_and_media import message
from pyrogram.types import *
from pyrogram.errors import (
    SessionPasswordNeeded, FloodWait,
    PhoneNumberInvalid, ApiIdInvalid,
    PhoneCodeInvalid, PhoneCodeExpired
)
import os

os.environ["REPLICATE_API_TOKEN"] = "10903c185f1d56f7a0284c28a421c2b3d5bbda46"
bot_token = "5481103194:AAG4QwvLnZ7k1_7NeLXxLh4226bFFHVqhiw"
api_id = 1530272
api_hash = "67da35e571d0cc9322f1520aa12c7a5b"
group_id = -1001895784719
app = Client("my_account", api_id=api_id, api_hash=api_hash,bot_token=bot_token)
@app.on_message(filters.command('start') & filters.private)
async def start(bot, message):
    await bot.send_message(message.chat.id,
                           reply_to_message_id=message.id,
                           text=f"Hello **{message.chat.first_name}!**\nI'm **Admin of telugu movies Channel**\nWant to Contact Onwer please wait for the reply",
                           reply_markup=InlineKeyboardMarkup(
                               [
                                   [
                                       InlineKeyboardButton(
                                           "Channel 💖", url="https://t.me/+NTyXOsgWd2tkOGM1"),
                                       InlineKeyboardButton(
                                           "BackUp Channel", url="https://t.me/backupchnltelugumovies")
                                   ]
                               ]
                           )
                           )

@app.on_message(filters.command('upload') & filters.private)
async def start(bot, message):
    text = message.text
    link = text.replace('/upload ','')
    req = httpx.get(content_url.format(link)).json()
    description = req['description']
    title = req['title']
    for l in req['other_links']:
      if "dood" in l['type']:
          dood_link = dood_upload(l['url'])
          img = img_quality(req['image'])
          image = image_uploader(img)
          await app.send_photo(group_id,photo=img,caption=f'title:\n**{title}**\nDescription:\n`{description}`\n\nFor **Ads in Group Contact** @telmovies_yssbot\nJoin Backup Channel',
          reply_markup=InlineKeyboardMarkup(
                  [
                      [
                          InlineKeyboardButton(
                              "Watch Now 👀 ", url=dood_link)
                      ],
                      [
                          InlineKeyboardButton(
                              "How To Open link", url="https://telegra.ph/HOW-TO-OPEN-SHORTEN-LINK-12-20")
                      ],
                    [
                          InlineKeyboardButton(
                              "How To Watch Without Ads", url="https://telegra.ph/HOW-TO-WATCH-ADD-FREE-12-20")
                    ],
                   [
                          InlineKeyboardButton(
                              "Backup Channel ❤️", url="https://t.me/backupchnltelugumovies")
                   ]
                      ]
              )
          )
          await bot.send_message(message.chat.id,
                                 reply_to_message_id=message.id,text='Movie Uploaded Sir')

@app.on_message(filters.command('isaka') & filters.private)
async def start(bot, message):
    if message.reply_to_message:
        txt=message.reply_to_message.caption
        text = txt.split("How to open links")[0]
        photo = message.reply_to_message.photo.file_id
        links = re.findall(r'https?://\S+', text)
        msg = await bot.send_message(message.chat.id, "Hello Sir I'm Working")
        a = 1
        for link in links:
            unshort =ome_mdisk(link)
            mdisk = gen_mdisk(unshort)
            text = re.sub(link, mdisk, text)
            ++a
        await msg.edit_text("Movie Uploaded")
        await bot.send_photo(group_id,
                             photo = photo,
                               reply_to_message_id=message.id, caption=text)

@app.on_inline_query()
async def search_video(client,query):
    search = []
    searc_url = "https://movierulz.vercel.app/search?query={}"
    result = query.query.strip()
    if result != "" and len(result) > 2:
        try:
            response = httpx.get(searc_url.format(result)).json()['data']
            async with httpx.AsyncClient() as client:
                get_url = "https://movierulz.vercel.app/get?url={}"
                tasks = [client.get(get_url.format(i['link'])) for i in response]
                responses = await asyncio.gather(*tasks)
            for i in responses:
                i = i.json()
                search.append(
                    InlineQueryResultPhoto(
                        title=i['title'],
                        caption=f"Title:\n{i['title']}\nDescrition:\n{i['description']}\nLink: `{i['url']}`",
                        description=i['description'],
                        photo_url=i['image']))
        except:
            search.append(
                InlineQueryResultPhoto(
                    title="Search Movie...",
                    description="Search movies from movierulz",
                    photo_url="https://i.ibb.co/gTw0cMZ/z-U0eo-JMFzt-Xv-Vk-PNst0-E62-JQCK-K7-XFEQC046-DF809-Ne8a-ZC1-Zn-Pw-JGuit-CE9-AMPr-U.jpg"))
    else:
        search.append(
            InlineQueryResultPhoto(
                title="Search Movie...",
                description="Search movies from movierulz",
                photo_url="https://i.ibb.co/gTw0cMZ/z-U0eo-JMFzt-Xv-Vk-PNst0-E62-JQCK-K7-XFEQC046-DF809-Ne8a-ZC1-Zn-Pw-JGuit-CE9-AMPr-U.jpg"))
    await query.answer(search)




app.run()
