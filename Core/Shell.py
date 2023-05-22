# -*- coding: utf-8 -*-



from datetime import datetime
from random import choice, randint
from string import ascii_letters
import subprocess
import os
import re
import time



class Shell:
    def __init__(self, language, code, bot_session, chat_id):
        language = language.title()
        if language in ["Python", "Shell", "C", "Cpp"]:
            code = self.__LoadConfig__(code)
            if code == False:
                bot_session.send_message(chat_id, "Can Not Load Config !!!")
            else:
                result = self.__Execute__(
                                           lang=language,
                                           code=(code["CODE"]),
                                           input_data=(code["INPUT"]),
                                           timeout=(code["TIMEOUT"])
                                         )
                if (result[1]) == "":
                    if (result[0]) == "":
                        result[0] = "Success !!!"
                    result[1] = "NULL"
                elif (result[0]) == "":
                    result[0] = "NULL"

                text = f"**==============================**\n**Language : {language}**\n**==============================**\n**Result :**\n\n\n{result[0]}\n**==============================**\n**Error :**\n\n{result[1]}\n**==============================**\n**Time(s) : {result[2]}**\n**==============================**"
                if (len(text)) >= 900:
                    file_name = self.__TempFileName__("txt")
                    with open(file_name, "w") as f:
                        f.write(text)
                    bot_session.send_document(chat_id, file_name)
                    os.remove(file_name)
                else:
                    bot_session.send_message(chat_id, text)

    def __LoadConfig__(self, code_data):
        config_data = re.findall("\W@.+", code_data)
        config_data = (list(map(str.strip, config_data)))
        config_optimize = {}
        for i in config_data:
            if (config_optimize.get("INPUT")) != None and (config_optimize.get("TIMEOUT")) != None:
                break
            else:
                attr_key = (((i.split("=")[0]).replace("@","").replace(" ","").strip()).upper())
                if (config_optimize.get(attr_key)) ==None:
                    if attr_key == "INPUT":
                        code_data = (code_data.replace(i,""))
                        value_data = (((i.split("=")[1]).strip()).split("$"))
                        value_data = (list(map(str.strip, value_data)))
                        value_data = (("\n".join([x for x in value_data])) + "\n")
                        value_data = value_data.encode()
                        config_optimize.update({attr_key:value_data})
                    elif attr_key == "TIMEOUT":
                        code_data = (code_data.replace(i,""))
                        try:
                            value_data = (eval(((i.split("=")[1]).strip())))
                            config_optimize.update({attr_key:value_data})
                        except Exception:
                            return False
        if (config_optimize.get("INPUT")) == None:
            config_optimize.update({"INPUT":None})
        if (config_optimize.get("TIMEOUT")) == None:
            config_optimize.update({"TIMEOUT":None})
        config_optimize.update({"CODE":(code_data.strip())})
        return config_optimize

    def __TempFileName__(self, file_format):
        return ((datetime.now().strftime("%Y%m%d%H%M%S")) + "-" + ("".join([(choice(ascii_letters)) for i in range(randint(10,20))])) + "." + file_format)

    def __Execute__(self, lang, code, input_data=None, timeout=None):
        start_time = time.time()
        if lang == "Python":
            file_name = self.__TempFileName__("py")
            with open(file_name, "w") as f:
                f.write(code)
            proc = subprocess.Popen(
                                     ["python3", file_name],
                                     stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE
                                   )
        elif lang in ["C", "Cpp"]:
            file_name = self.__TempFileName__((lang.lower()))
            with open(file_name, "w") as f:
                f.write(code)
            if lang == "C":
                compiler = "gcc"
            elif lang == "Cpp":
                compiler = "g++"
            proc = subprocess.Popen(
                                     [f"{compiler} {file_name} -o a.out && ./a.out"],
                                     stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     shell=True
                                   )
        elif lang == "Shell":
            proc = subprocess.Popen(
                                     [code],
                                     stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     shell=True
                                   )
        if timeout == None:
            if input_data == None:
                proc_result, proc_error = proc.communicate(b" ")
            else:
                proc_result, proc_error = proc.communicate(input_data)
            if lang in ["C", "Cpp", "Python"]:
                os.remove(file_name)
                if lang in ["C", "Cpp"]:
                    try:
                        os.remove("a.out")
                    except Exception:
                        pass
            end_time = time.time()
            proc = [proc_result.decode(), proc_error.decode(), ("%.2f" % (end_time - start_time))]
            return proc
        else:
            try:
                if input_data == None:
                    proc_result, proc_error = proc.communicate(b" ", timeout=timeout)
                else:
                    proc_result, proc_error = proc.communicate(input_data, timeout=timeout)
            except Exception:
                proc.kill()
                proc_result, proc_error = proc.communicate()
            if lang in ["C", "Cpp", "Python"]:
                os.remove(file_name)
                if lang in ["C", "Cpp"]:
                    try:
                        os.remove("a.out")
                    except Exception:
                        pass
            end_time = time.time()
            proc = [proc_result.decode(), proc_error.decode(), ("%.2f" % (end_time - start_time))]
            return proc

