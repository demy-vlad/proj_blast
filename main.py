from requests.models import Response
from telebot import types
from random import choice
from string import ascii_uppercase
from config import bot
from loguru import logger

import time

import lxml
import requests
from bs4 import BeautifulSoup


# copy_rid = ["CH49FZYV013", "CH7RTGVB013"]
copy_rid = []
array_get_rid = []

# bot.remove_webhook()

global blastn
import threading

import text  
text = text

logger.debug("Bot is running")
 
# def main():  message.chat.id, message.chat.username, message.chat.last_name, message.chat.first_name,
        #    message.chat.photo
@bot.message_handler(commands=['start'])
def start(message):
    logger.debug(f"{message.chat.id, message.chat.username, message.chat.last_name, message.chat.first_name} - click: start")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu = types.KeyboardButton(text.start_menu)
    recent_result = types.KeyboardButton(text.recent_result)
    # faq = types.KeyboardButton("💡 FAQ")
    markup.add(menu)
    markup.add(recent_result)
    # markup.add(faq)
    text1 = text.text1
    text2 = text.text2
    bot.send_message(message.chat.id, text1 + text2, reply_markup=markup, parse_mode= "Markdown")


@bot.message_handler(content_types=['text'])
def founded_menu_faq(message):
    if message.text == text.start_menu:
        logger.debug(f"{message.chat.id} - click: {text.start_menu}")
        if not array_get_rid:
            keyboard = types.InlineKeyboardMarkup()            
            blastn = types.InlineKeyboardButton("➕ Blastn", callback_data='blastn_s')
            blastp = types.InlineKeyboardButton("➕ Blastp", callback_data='blastp_s')
            blastx = types.InlineKeyboardButton("➕ Blastx", callback_data='blastx_s')
            tblastn = types.InlineKeyboardButton("➕ Tblastn", callback_data='tblastn_s')
            tblastx = types.InlineKeyboardButton("➕ Tblastx", callback_data='tblastx_s')

            keyboard.add(blastn, blastp)
            keyboard.add(blastx, tblastn)
            keyboard.add(tblastx)
            bot.send_message(message.chat.id, text.mess1+text.mess2+text.mess3+text.mess4+text.mess5 , reply_markup=keyboard, parse_mode= "Markdown")
        else:
            bot.send_message(message.chat.id, text=text.faq_error)

    elif message.text == text.recent_result:
        logger.debug(f"{message.chat.id} - click: {text.recent_result}")
        threading.Thread(target = recent_result2(message), args=(2,)).start()
        # recent_result2(message)
    elif message.text == "FAQ":
        # recent_result1(message)
        mess = "Информация о FAQ"
        bot.send_message(message.chat.id, text=mess)
    else:
        bot.send_message(message.chat.id, text.select_action)

@bot.callback_query_handler(func=lambda call:True)
def homo_sapiens_hucleotide(call):
    if call.data == "blastn_s":
        global blastn
        global d_blast
        d_blast = "nt"
        blastn = "blastn"
        hseq = "TTTTTTTTTTAAATGCCCATAGTTTTT"
        msg = bot.send_message(call.message.chat.id, text=f"{text.homo_sapiens}{text.hseq} {hseq}", parse_mode= "Markdown")
        bot.register_next_step_handler(msg, accession_number_blastn)
    elif call.data == "blastp_s":
        blastn = "blastp"
        d_blast = "nr"
        msg = bot.send_message(call.message.chat.id, text=f"{text.homo_sapiens}", parse_mode= "Markdown")
        bot.register_next_step_handler(msg, accession_number_blastn)
    elif call.data == "blastx_s":
        blastn = "blastx"
        d_blast = "nr"
        msg = bot.send_message(call.message.chat.id, text=f"{text.homo_sapiens}", parse_mode= "Markdown")
        bot.register_next_step_handler(msg, accession_number_blastn)
    elif call.data == "tblastn_s":
        blastn = "tblastn"
        d_blast = "nr/nt"
        msg = bot.send_message(call.message.chat.id, text=f"{text.homo_sapiens}", parse_mode= "Markdown")
        bot.register_next_step_handler(msg, accession_number_blastn)
    elif call.data == "tblastx_s":
        blastn = "tblastx"
        d_blast = "nr/nt"
        msg = bot.send_message(call.message.chat.id, text=f"{text.homo_sapiens}", parse_mode= "Markdown")
        bot.register_next_step_handler(msg, database)
 
def accession_number_blastn(message): #Получаем ДНК
    global accession_FASTA
    accession_FASTA = message.text
    logger.info(accession_FASTA)
    # print(accession_FASTA)
    msg = bot.send_message(message.chat.id, text=text.accession_FASTA, parse_mode= "Markdown")
    bot.register_next_step_handler(msg, query_subrange_form_blastn)

def query_subrange_form_blastn(message): #Получаем диапазон Form
    global qs_from
    qs_from = message.text
    logger.info(qs_from)
    # print(qs_from)
    msg = bot.send_message(message.chat.id, text=text.qs_from, parse_mode= "Markdown")
    bot.register_next_step_handler(msg, query_subrange_to_blastn)

def query_subrange_to_blastn(message): #Получаем диапазон To
    global qs_to
    qs_to = message.text
    logger.info(qs_to)
    # print(qs_to)
    get_rid(message)
    # database(message)

def database(message): #Выбираем БД
    keyboard = types.InlineKeyboardMarkup()            
    nt = types.InlineKeyboardButton("Сбор нуклеотидов", callback_data='nt_s')
    nr = types.InlineKeyboardButton("Неизбыточный", callback_data='nr_s')
    refseq_rna = types.InlineKeyboardButton("Контрольные последовательности стенограммы NCBI", callback_data='refseq_rna_s')
    pdbnt = types.InlineKeyboardButton("База данных нуклеотидов PDB", callback_data='pdbnt_ss')

    keyboard.add(nt)
    keyboard.add(nr)
    keyboard.add(refseq_rna)
    keyboard.add(pdbnt)
    text1 = "Доступные базы данных *BLAST*:"
    bot.send_message(message.chat.id, text1 ,reply_markup=keyboard, parse_mode= "Markdown")
    logger.info(keyboard)

@bot.callback_query_handler(func=lambda call:database)
def homo_sapiens_hucleotideww(call):
    print(call.data)
    if data in "nt_s":
        global d_blast
        d_blast = "nt"
        msg = bot.send_message(call.message.chat.id, text=f"Ssss", parse_mode= "Markdown")
        bot.register_next_step_handler(msg, get_rid)
    elif call.data == "nr_s":
        d_blast = "nr"
        bot.register_next_step_handler(call.message.chat.id, get_rid)
    elif call.data == "refseq_rna_s":
        d_blast = "refseq_rna"
        bot.register_next_step_handler(call.message.chat.id, get_rid)
    elif call.data == "pdbnt_s":
        d_blast = "pdbnt"
        bot.register_next_step_handler(call.message.chat.id, get_rid)

def get_rid(message): #Узнаём RID
    bot.send_message(message.chat.id, text.get_rid)
    global headers
    headers = {
        "accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    }

# https://blast.ncbi.nlm.nih.gov/Blast.cgi?QUERY=TTTTTTTTTTAAATGCCCATAGTTTTT&DATABASE=nr&DATABASE=nt&PROGRAM=blastx&CMD=Put&QUERY_FROM=1&QUERY_TO=25
    url = requests.get(
        f"https://blast.ncbi.nlm.nih.gov/Blast.cgi?QUERY={accession_FASTA}&DATABASE={d_blast}&PROGRAM={blastn}&CMD=Put&QUERY_FROM={qs_from}&QUERY_TO={qs_to}", headers=headers)
    logger.info(f"https://blast.ncbi.nlm.nih.gov/Blast.cgi?QUERY={accession_FASTA}&DATABASE={d_blast}&PROGRAM={blastn}&CMD=Put&QUERY_FROM={qs_from}&QUERY_TO={qs_to}")
    # print(url)   
    if url.status_code !=200:
        logger.info(f"Status code: {url}")
    else:
        logger.info(f"Status code: {url}")
        global soup
        soup = BeautifulSoup(url.text, "lxml")
        global rid

        rid = soup.find(id="rid")["value"]
        title = soup.find('title')
        logger.info(f"Get title: {title.text}")
        logger.info(f"Get RID: {rid}")
        array_get_rid.append(rid)
        copy_rid.append(rid)
        logger.info(f"Status array: {array_get_rid}")

        if rid != "":
            bot.send_message(message.chat.id, f"{text.get_rid_mess}", parse_mode= "Markdown")
            url = requests.get(
                f"https://blast.ncbi.nlm.nih.gov/Blast.cgi?QUERY={accession_FASTA}&DATABASE=nt&PROGRAM={blastn}&CMD=Get&RID={rid}&QUERY_FROM={qs_from}&QUERY_TO={qs_to}", headers=headers)
            threading.Thread(target = get_result(message), args=(50,)).start()
        else:
            bot.send_message(message.chat.id, text.not_found, parse_mode= "Markdown")
            array_get_rid.remove(rid)
            copy_rid.remove(rid)


def get_result(message):
    for i in array_get_rid:
        logger.info(f"Status result RID: {i}")
        url = requests.get(f"https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Get&RID={i}")
        soup = BeautifulSoup(url.text, "lxml")
        time.sleep(5)
        title = soup.find('title')
        logger.info(f"Title 2: {title.text}")

        if title.text == "NCBI Blast:Nucleotide Sequence":
            err_significant_similarity = soup.find(id= "noResMsg")
            try:
                if err_significant_similarity != "No significant similarity found. For reasons why,click here":
                    title = soup.find('title')
                    logger.info(f"Result new title : {title.text}")
                    new_Title(message, i)
                else:
                    try:
                        array_get_rid.remove(i) 
                        logger.info(f"Remove array get rid: {title.text}")
                        bot.send_message(message.chat.id, f"{text.get_result_not_found}\nRID: {i}")
                    except ValueError:
                        logger.exception("ValueError")
            except NameError:
                logger.exception("AttributeError")
    
        else:
            logger.info("Respons [def get_result]")
            get_result(message)

def new_Title(message, i):
    try:
        logger.info("Download document")
        file_url = (
                f"https://blast.ncbi.nlm.nih.gov/Blast.cgi?RESULTS_FILE=on&RID={i}&FORMAT_TYPE=Text&FORMAT_OBJECT=Alignment&DESCRIPTIONS=10&ALIGNMENTS=10&CMD=Get&DOWNLOAD_TEMPL=Results_All&ADV_VIEW=on")         
        r = requests.get(file_url, stream = True, headers=headers)
        
        with open(f"file\{i}.txt","wb") as pdf:
                for chunk in r.iter_content(chunk_size=1024):
                        '''
                        writing one chunk at a time to pdf file
                        '''
                        if chunk:
                            pdf.write(chunk)

        try:    
            array_get_rid.remove(i)
            logger.info(f"Remove get RID: {array_get_rid}")
        except ValueError:
            logger.exception("ValueError")
        
        text_file = open(f"file\{i}.txt").readlines()  
        number_of_elements_array = len(text_file)
        logger.info(f"Number of elements array: {array_get_rid}")
        if number_of_elements_array > 16:       
            get_text_file = f"{text_file[0]}{text_file[3]}\n{text_file[21]}{text_file[23]}{text_file[24]}{text_file[25]}{text_file[26]}{text_file[27]}"
            bot.send_message(message.chat.id, get_text_file)
            txt = open(f"file\{i}.txt")
            bot.send_document(message.chat.id, txt)
            keyboard = types.InlineKeyboardMarkup()
            url = types.InlineKeyboardButton(text=text.result_search, url=f"https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Get&RID={i}")
            keyboard.add(url)
        else:
            bot.send_message(message.chat.id, f"{text.get_result_not_found}")
        
    except IndexError:
        bot.send_message(message.chat.id, f"{text.get_result_not_found}\nRID: {rid}")

def recent_result2(message):
    
    try:
        logger.info(f"Result search: {copy_rid}")
        if not copy_rid:
                bot.send_message(message.chat.id, text=text.recent_not_found)
        else:
            for array_rid in copy_rid:
                url = requests.get(f"https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Get&RID={array_rid}", headers=headers)
                soup = BeautifulSoup(url.text, "lxml")
                title = soup.find('title')

                keyboard = types.InlineKeyboardMarkup()
                url = types.InlineKeyboardButton(text=text.result_search, url=f"https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Get&RID={array_rid}")
                keyboard.add(url)

                if title.text == "NCBI Blast:Nucleotide Sequence":
                    txt = open(f"file\{array_rid}.txt")
                    bot.send_document(message.chat.id, txt)
                    bot.send_message(message.chat.id, f"🟢 {text.request} ID: {array_rid} - {text.done}", parse_mode= "Markdown", reply_markup=keyboard)

                else:
                    bot.send_message(message.chat.id, f"🔴 {text.request} ID: {array_rid} - {text.running}", parse_mode= "Markdown", reply_markup=keyboard)
    except NameError:
        logger.exception("NameError")
        bot.send_message(message.chat.id, f"{text.recent_not_found}", parse_mode= "Markdown")
    

bot.polling(none_stop=True)