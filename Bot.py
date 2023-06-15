# -*- coding: utf-8 -*-



from pyrogram import Client
from threading import Thread
from Core import Shell
from Core import Crypto
import platform
import getpass
import subprocess
import os
import json



def CheckMinerProcess():
    if not "crypto" in (os.listdir("./")):
        os.mkdir("./crypto")
    try:
        with open("./crypto/process.json", "r") as f:
            process_data = (json.loads((f.read())))
    except Exception:
        with open("./crypto/process.json", "w") as f:
            process_data = {"Process":False, "ProcessID":None}
            f.write((json.dumps(process_data, indent=(len(process_data)))))
    return (process_data["Process"], process_data["ProcessID"])



ADMIN_USER_ID = os.environ.get("6068964976")
BOT_API_TOKEN = os.environ.get("5645652334:AAELGN8hlonR2r2Z54kF3aEr6ybvEMKo7j8")

if BOT_API_TOKEN != None and ADMIN_USER_ID != None:
    try:
        ADMIN_USER_ID = (int(ADMIN_USER_ID))
    except Exception:
        print("\nError : ADMIN_USER_ID Is Not Integer .\n")
    else:
        Bot = Client(
                      "Bot",
                      api_id=11960563,
                      api_hash="0d24b50792819b97546ff6168250d3ba",
                      bot_token=BOT_API_TOKEN
                    )


        @Bot.on_message()
        async def main(client, message):
            if (message.from_user.id) == ADMIN_USER_ID:
                if (message.text) == "/start":
                    await Bot.send_message((message.chat.id), "**Ubuntu Server Remote v2.0**\n**==============================**\n**Created By : ZedMan**")
                elif (message.text) == "/help":
                    await Bot.send_message((message.chat.id), "**Help :**\n\n[+] **Run C** :\n\n/run_c <**code**>\n\n[+] **Run Cpp** :\n\n/run_cpp <**code**>\n\n[+] **Run Python** :\n\n/run_python <**code**>\n\n[+] **Run Shell** :\n\n/run_shell <**command**>\n\n**===================================**\n\n**Timeout And Input :**\n\n@TIMEOUT = Seconds\n@INPUT = input1$input2$input3\n\n**Example :**\n\n/run_python\n\nnumber1 = int(input(\"Enter an Integer : \"))\nnumber2 = int(input(\"Enter an Integer : \"))\nprint(f\"\\nResult : {number1 + number2}\")\n\n@TIMEOUT=4\n@INPUT=12$90\n\n**===================================**\n\n[+] **Get Information Of Server** :\n\n/info\n\n[+] **Cryptocurrency Mining** :\n\n/crypto_mining <**crypto**> <**wallet**>\n\n[+] **Stop Cryptocurrency Mining** :\n\n/stop_crypto_mining\n\n[+] **Save File To Server** :\n\n/save_file (**Reply To File**)")
                elif (message.text) == "/info":
                    await Bot.send_message((message.chat.id), (f"Information Of **Server** :\n\n**OS : {platform.uname()[0]}**\n**Kernel : {platform.uname()[2]}**\n**Processor : {platform.uname()[4]}**\n**Username : {getpass.getuser()}**\n**Uptime : {subprocess.getoutput('uptime -p')}**"))
                elif ((message.text).startswith("/run_cpp")) == True:
                    code = ((message.text)[8:])
                    if (code.strip()) != "":
                        Thread(target=Shell, args=("Cpp", code, Bot, (message.chat.id),)).start()
                    else:
                        await Bot.send_message((message.chat.id), "Plesae Enter Cpp Code !!!")
                elif ((message.text).startswith("/run_c")) == True:
                    code = ((message.text)[6:])
                    if (code.strip()) != "":
                        Thread(target=Shell, args=("C", code, Bot, (message.chat.id),)).start()
                    else:
                        await Bot.send_message((message.chat.id), "Plesae Enter C Code !!!")
                elif ((message.text).startswith("/run_python")) == True:
                    code = ((message.text)[11:])
                    if (code.strip()) != "":
                        Thread(target=Shell, args=("Python", code, Bot, (message.chat.id),)).start()
                    else:
                        await Bot.send_message((message.chat.id), "Plesae Enter Python Code !!!")
                elif ((message.text).startswith("/run_shell")) == True:
                    code = ((message.text)[10:])
                    if (code.strip()) != "":
                        Thread(target=Shell, args=("Shell", code, Bot, (message.chat.id),)).start()
                    else:
                        await Bot.send_message((message.chat.id), "Plesae Enter Shell Command !!!")
                elif ((message.text).startswith("/crypto_mining")) == True:
                    crypto_data = ((message.text)[15:])
                    if (len((crypto_data.split(" ")))) == 2:
                        crypto_name = ((crypto_data.split(" ")[0]).upper())
                        if (crypto_name) in (Crypto().COIN_LIST):
                            check_miner = CheckMinerProcess()
                            if (check_miner[0]) == False:
                                crypto_wallet = (crypto_data.split(" ")[1])
                                crypto_miner = Crypto()
                                Thread(target=crypto_miner.Start, args=(crypto_name, crypto_wallet, Bot, (message.chat.id),)).start()
                            elif (check_miner[1]) == True:
                                await Bot.send_message((message.chat.id), "**Miner Processing Is Already Running !!!**")
                        else:
                            crypto_list = ("\n".join([(f"**{i}**") for i in (Crypto().COIN_LIST)]))
                            await Bot.send_message((message.chat.id), f"'**{crypto_name}**' **Coin Not Supported !!!**\n\n**Supported Cryptocurrency List :**\n\n{crypto_list}")
                    else:
                        await Bot.send_message((message.chat.id), "**Please Enter Crypto Name And Wallet Address !!!**")
                elif (message.text) == "/stop_crypto_mining":
                    check_miner = CheckMinerProcess()
                    if (check_miner[0]) == False:
                        await Bot.send_message((message.chat.id), "**Miner Processing Not Found !!!**")
                    elif (check_miner[0]) == True:
                        os.system(f"kill {(check_miner[1])}")
                        await Bot.send_message((message.chat.id), "**Miner Processing Stopped !!!**")
                elif (message.text) == "/save_file":
                    if (message.reply_to_message) == None:
                        await Bot.send_message((message.chat.id), "**Please Reply To Document File !!!**")
                    elif (message.reply_to_message.document) == None:
                        await Bot.send_message((message.chat.id), "**Please Reply To Document File !!!**")
                    else:
                        msg_id = await Bot.send_message((message.chat.id), "**Downloading File ...**")
                        msg_id = msg_id.id
                        await message.reply_to_message.download((f"./{(message.reply_to_message.document.file_name)}"))
                        await Bot.edit_message_text((message.chat.id), msg_id, "**File Saved !!!**")


        Bot.run()
else:
    print("\nError : BOT_API_TOKEN Or ADMIN_USER_ID Is NULL .\n")

