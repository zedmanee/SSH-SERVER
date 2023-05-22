# -*- coding: utf-8 -*-



from requests import get
from datetime import datetime
from time import time, sleep
from string import ascii_letters
from random import randint, choice
import subprocess
import os
import json
import tarfile
import re



class Crypto:
    def __init__(self, miner_path="./", miner_folder="crypto"):
        self.POOL_ADDRESS = "rx.unmineable.com:3333"
        self.COIN_LIST = [
                            "BTC", "BCH", "ETH", "ETC",
                            "BNB", "LTC", "DOGE", "SOL",
                            "DASH", "XMR","TRX", "USDT",
                            "DGB", "SHIB", "EOS"
                         ]
        self.XMRIG_VERSION = "6.18.1"
        self.MINER_PATH = miner_path
        self.MINER_FOLDER = miner_folder
        self.MINER_FULL_PATH = (self.MINER_PATH + self.MINER_FOLDER + "/")

    def __CheckMiner__(self):
        if not self.MINER_FOLDER in (os.listdir(self.MINER_PATH)):
            os.mkdir(self.MINER_FULL_PATH)
            return False
        elif "config.json" in (os.listdir(self.MINER_FULL_PATH)) and "crypto" in (os.listdir(self.MINER_FULL_PATH)):
            return True
        else:
            return False

    def __MinerDownloader__(self):
        try:
            res = get(
                       (f"https://github.com/xmrig/xmrig/releases/download/v{(self.XMRIG_VERSION)}/xmrig-{(self.XMRIG_VERSION)}-focal-x64.tar.gz")
                     )
        except Exception:
            return False
        else:
            if res.status_code == 200:
                res = res.content
                with open((self.MINER_PATH + "crypto.tar.gz"), "wb") as f:
                    f.write(res)
                file_data = self.__MinerFileReader__((self.MINER_PATH + "crypto.tar.gz"))
                os.remove((self.MINER_PATH + "crypto.tar.gz"))
                with open((self.MINER_FULL_PATH + "crypto"), "wb") as f:
                    f.write(file_data["xmrig"])
                with open((self.MINER_FULL_PATH + "config.json"), "w") as f:
                    file_data["config.json"] = (json.loads((file_data["config.json"])))
                    f.write((json.dumps((file_data["config.json"]), indent=(len(file_data["config.json"])))))
                return True
            else:
                return False

    def __MinerFileReader__(self, file_name):
        file_list = {}
        with tarfile.open(file_name, "r:gz") as f:
            for file in (f.getmembers()):
                file_name = (((file.name).split("/"))[-1])
                if file_name in ["config.json", "xmrig"]:
                    file_list.update({file_name:((f.extractfile(file)).read())})
        return file_list

    def __GetWorkerName__(self):
        _char_data = ascii_letters + "0123456789"
        return ("Linux" + ("".join([(choice(_char_data)) for i in range((randint(10,18)))])))

    def __ChangeConfig__(self):
        with open((self.MINER_FULL_PATH + "config.json"), "r") as f:
            config_data = json.load(f)
        config_data["pools"][0]["url"] = self.POOL_ADDRESS
        config_data["pools"][0]["user"] = (f"{(self.COIN)}:{(self.WALLET)}.{(self.WORKER_NAME)}")
        with open((self.MINER_FULL_PATH + "config.json"), "w") as f:
            f.write((json.dumps(config_data, indent=(len(config_data)))))

    def __ChangeProcessFile__(self, process_status, process_id=None):
        with open((self.MINER_FULL_PATH + "process.json"), "w") as f:
            process_data = {"Process":process_status, "ProcessID":process_id}
            f.write((json.dumps(process_data, indent=(len(process_data)))))

    def __GetMiningValue__(self):
        try:
            res = get(
                       (f"https://api.unmineable.com/v4/address/{(self.WALLET)}/?coin={(self.COIN)}")
                     )
        except Exception:
            return False
        else:
            if res.status_code == 200:
                try:
                    res = res.json()
                except Exception:
                    return False
                else:
                    return {"MiningValue":(res["data"]["balance"]), "MinPay":(res["data"]["payment_threshold"])}
            else:
                return False

    def __StartMiner__(self, Bot, ChatID):
        os.system(f"chmod +x {(self.MINER_FULL_PATH)}crypto")
        try:
            os.remove(f"{(self.MINER_FULL_PATH)}process.log")
        except Exception:
            pass
        proc = subprocess.Popen(
                                 [f"{(self.MINER_FULL_PATH)}crypto --log-file=\"{(self.MINER_FULL_PATH)}process.log\" --config=\"{(self.MINER_FULL_PATH)}config.json\""],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 shell=True
                               )
        process_start_time = time()
        process_start_date = datetime.now().strftime("%Y/%m/%d - %H:%M:%S")
        msg_id = Bot.send_message(ChatID, f"**Start Miner ⚡️ ...**\n\n**Start Date/Time ⏰ : {process_start_date}**\n**XMRIG 🛠 Version : {(self.XMRIG_VERSION)}**\n**Crypto 💰 : {(self.COIN)}**\n**Wallet Address 💳 :** `{(self.WALLET)}`\n**Mining ⛏ Process Time(s) : {('%.2f' % (time() - process_start_time))}s**")
        msg_id = msg_id.id
        self.__ChangeProcessFile__(
                                    process_status=True,
                                    process_id=(proc.pid + 1)
                                  )
        while ((proc.poll()) != 0):
            sleep((randint(90,150)))
            with open((self.MINER_FULL_PATH + "process.log"), "r") as f:
                log_data = f.read()
            miner_hashrate = re.findall("\Wspeed.+", log_data)
            if miner_hashrate != []:
                miner_hashrate = ((((miner_hashrate[-1]).split("max"))[-1]).strip())
            else:
                miner_hashrate = "NULL"
            mining_value = self.__GetMiningValue__()
            if mining_value == False:
                paymin = "NULL"
                mining_value = "NULL"
            else:
                paymin = mining_value["MinPay"]
                mining_value = mining_value["MiningValue"]
            Bot.edit_message_text(ChatID, msg_id, f"**Status :** 🔋\n**Start Date/Time ⏰ : {process_start_date}**\n**XMRIG 🛠 Version : {(self.XMRIG_VERSION)}**\n**Crypto 💰 : {(self.COIN)}**\n**Wallet Address 💳 :** `{(self.WALLET)}`\n**Mining ⛏ Process Time(s) : {('%.2f' % (time() - process_start_time))}s**\n**Mining Hashrate(s) ⚡️ : {miner_hashrate}**\n**Mining Value 💎 : {mining_value} {(self.COIN)}**\n**Payment Minimum 💲 : {paymin} {(self.COIN)}**")
        self.__ChangeProcessFile__(process_status=False)
        Bot.edit_message_text(ChatID, msg_id, f"**Status :** 🪫\n**Start Date/Time ⏰ : {process_start_date}**\n**XMRIG 🛠 Version : {(self.XMRIG_VERSION)}**\n**Crypto 💰 : {(self.COIN)}**\n**Wallet Address 💳 :** `{(self.WALLET)}`\n**Mining ⛏ Process Time(s) : {('%.2f' % (time() - process_start_time))}s**")

    def Start(self, coin_name, wallet_address, bot, chat_id):
        if (coin_name.upper()) in (self.COIN_LIST):
            self.COIN = (coin_name.upper())
            self.WALLET = wallet_address
            self.WORKER_NAME = self.__GetWorkerName__()
            if (self.__CheckMiner__()) == True:
                self.__ChangeConfig__()
                self.__StartMiner__(bot, chat_id)
            elif (self.__CheckMiner__()) == False:
                msg_id = bot.send_message(chat_id, "**Start Downloading Miner File ...**")
                msg_id = msg_id.id
                download_result = self.__MinerDownloader__()
                if download_result == True:
                    bot.edit_message_text(chat_id, msg_id, "**Miner File Downloaded !!!**")
                    self.__ChangeConfig__()
                    self.__StartMiner__(bot, chat_id)
                elif download_result == False:
                    bot.edit_message_text(chat_id, msg_id, "**Failed To Downloading Miner File !!!**")

