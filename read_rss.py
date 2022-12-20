import feedparser
import random
import requests
import datetime

'''
https://api.telegram.org/bot111:222/sendMessage?chat_id=@channelName&text=123
https://stackoverflow.com/questions/33858927/how-to-obtain-the-chat-id-of-a-private-telegram-channel
https://www.datasciencelearner.com/how-to-read-rss-feed-in-python/
https://www.delftstack.com/pt/howto/python/python-shuffle-array/
'''

msgs_hora = {9:  "O que acha de rezar um Pai Nosso?",
             12: "\n\nSeria possível uma pausa no que está fazendo para rezar o Angelus?\n\nhttps://www.vaticannews.va/pt/oracoes/angelus--a-trindades-.html",
             #12: "\n\nSeria possível uma pausa no que está fazendo para rezar o Regina Caeli?\n\nhttps://www.vaticannews.va/pt/oracoes/rainha-do-ceu-.html",
             18: "Vamos rezar o terço? Ta sem tempo? Então uma Ave Maria!!",
             17: "Conhece nosso bot? Santo do dia, Exame de Consciencia, Catecismo! @anjogabriel_bot",
             20: "\n\nO que acha de se preparar para um exame de consciencia?\n\nhttps://opusdei.org/pt-pt/article/audio-exame-de-consciencia-diario-em-3-minutos/"}


#telegram bot key
#t.me/anjogabriel_bot
bot_key = ""
chat_id = ""
url_msg = "https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s"
source_urls_cadastradas = "urls_cadastradas.txt"
source_urls_feeds = "feeds.txt"


def hora_brasil():
    from datetime import datetime, timedelta

    d = datetime.now() - timedelta(hours=3, minutes=0)

    return d


def gera_lista_urls_cadastradas(source_file):
    lista_urls_cadastradas = []
    f = open(source_file, "r")
    i = f.readline()
    while i:
        linha = i.strip()
        lista_linha = linha.split("|")
        url = lista_linha[0]
        lista_urls_cadastradas.append(url)
        i = f.readline()
    return lista_urls_cadastradas

def grava_url_cadastro(source_file, url):
    agora = datetime.datetime.now()
    lista_urls_cadastradas = []
    f = open(source_file, "a")
    f.write("%s|%s\n" % (url, agora))


def gera_lista_feed(source_file):
    lista_urls_feeds = []
    f = open(source_file, "r")
    i = f.readline()
    while i:
        linha = i.strip()
        lista_urls_feeds.append(linha)
        i = f.readline()
    return lista_urls_feeds

def bot_sender(url_sender_par, bot_key_par, chat_id_par, msg_par):
    res = requests.get(url_sender_par % (bot_key_par, chat_id_par, msg_par))
    pass


def envia_urls_channel(source_urls_cadastradas_par, feed_list_par):
    lista_urls_cadastradas = gera_lista_urls_cadastradas(source_urls_cadastradas_par)
    lista_para_envios_url = []
    for feed_url in feed_list_par:
        Feed = feedparser.parse(feed_url)
        pointer_list = Feed.entries
        print(pointer_list)
        for pointer in pointer_list:
            #print (pointer.summary)
            #print (pointer.link)

            url = pointer.link

            if url not in lista_urls_cadastradas:
                grava_url_cadastro(source_urls_cadastradas_par, url)
                print(url)
                lista_para_envios_url.append(url)
    random.shuffle(lista_para_envios_url)

    for url in lista_para_envios_url:
        bot_sender(url_msg, bot_key, chat_id, url)


    #eventos por hora
    agora_brasil = datetime.datetime.now() - datetime.timedelta(hours=3)
    hora = agora_brasil.hour

    try:
        bot_sender(url_msg, bot_key, chat_id, msgs_hora[hora])
    except:
        print("nao há msgs especificas para essa hora")


    print("fim do envio")





def envia_primeiro_post():
    lista = gera_lista_urls_cadastradas(source_urls_cadastradas)
    random.shuffle(lista)
    for url in lista:
        print(url)
        bot_sender(url_msg, bot_key, chat_id, url)

#geral lista de feeds
feed_list = gera_lista_feed(source_urls_feeds)


envia_urls_channel(source_urls_cadastradas, feed_list)
#envia_primeiro_post()
