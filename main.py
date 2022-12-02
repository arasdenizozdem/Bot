import discord
from discord.ext import commands
from discord.ext.commands import Bot
from api import grabdata
import json
import datetime

intent = discord.Intents.default()
intent.members = True
intent.message_content = True

time=datetime.datetime.now()
if len(str(time.day))>1:
    date=str(time.day)+"/"+str(time.month)+"/"+str(time.year)
else:
    date="0"+str(time.day)+"/"+str(time.month)+"/"+str(time.year)
print(date)
Bot = Bot(command_prefix="!",intents=intent)


@Bot.event
async def on_ready():
    print("Ben Hazırım!")


@Bot.command()
async def oranlar(ctx, date=date):
    try:
        dictionary=grabdata(date)
        await ctx.send(str(dictionary))
    except:
        await ctx.send("Maç devam ederken herhangi bir bahis oynananamaz. | Bahis Suresi/14. Ayet")
@Bot.command()
async def oyna(ctx, date, matchcode, bet, money:int):
    genel_maç_bilgisi=""
    #Para Kontrolü
    with open("para.json", "r") as f:
        jsonobj=json.loads(f.read())
    user_id = str(ctx.author.id)
    balance=int(jsonobj[user_id])
    if money > balance:
        await ctx.send("Lütfen düzgün bir para miktarı seçin.")
        return False
    else:
        new_balance=balance-money
        jsonobj[user_id]=new_balance
        new_jsonobj= json.dumps(dict(jsonobj))
        with open("para.json", "w") as f:
            f.write(new_jsonobj)
    #Maç Bilgisi Çekme
    match = ""
    data_api=grabdata(date)
    data_api[-1]["matchcode"]=str(data_api[-1]["matchcode"]).replace("[[","")
    for i in data_api:
        if i["matchcode"] == str(matchcode):
            genel_maç_bilgisi=i
            match=str(i["hometeam"]+"-"+i["awayteam"]).replace('"',"")
    for i in genel_maç_bilgisi:
        genel_maç_bilgisi[i]=genel_maç_bilgisi[i].replace('"',"")
    #Genel Data Hesaplama
    new_bet=genel_maç_bilgisi[str(bet)]
    dataya_dönüşüm={user_id:[bet,new_bet]}
    await ctx.send("{} maçına {} bahsi {} oranıyla başarıyla oynandı.".format(match, str(bet).upper(), new_bet))

@Bot.command()
async def hesap(ctx):
    user_id = str(ctx.author.id)
    with open("para.json", "r") as f:
        jsonobj=json.loads(f.read())
    await ctx.send(jsonobj[user_id])

@Bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandNotFound):
    await ctx.send("Böyle bir komut bulunmamakta")

Bot.run("MTA0NjgxODI2NzIxMTI0MzU3MA.GuKy9G.V11YIaRi3pmCEKoH_JlTomYOmJTafzx5wIRtNg")