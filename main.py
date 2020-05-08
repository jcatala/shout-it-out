#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import configparser
from pathlib import Path
import textwrap
import argparse
import sys
import telegram


def check_args():
    parser = argparse.ArgumentParser(description = "Simple Shout-it-out telegram notificator")
    parser.add_argument('-c', '--config',help="Full path to config file (default is ~/.SIO.conf")
    parser.add_argument('-i', '--infile',help="Send a text file (default is stdin)")
    parser.add_argument('-v', '--verbose',required = False, help="Turn on the verbose mode", action="store_true",default=False)
    parser.add_argument('-F', '--filter',required = False, help="Add a filter before sending the message (string: default: None)",default=False)
    parser.add_argument('-f', '--follow', required=False,
                        help="Send one line at a time", action="store_true", default=False)
    parser.add_argument('-m', '--markdown', required=False,
                        help="Force markdown on the entire message, if is not, do it by yourself adding backquotes", action="store_true", default=False)
    return vars(parser.parse_args())


def get_chat_id(bot):
    chat_id = bot.get_updates()[-1]['message']['chat']['id']
    return chat_id


def send_message_byfile(bot, file_name,chat_id = ""):
    try:
        chat_id = get_chat_id(bot)
    except:
        print("Error getting chat id, using {} from the config file".format(chat_id))
    with open(file_name, "r") as a:
        content = a.read().strip('\n')
    payload = textwrap.fill(content,256).split('\n')
    for k in payload:
        if k != "":
            bot.send_message(chat_id = chat_id, text = str(k))
    return True

def send_message_follow(bot,args,chat_id = ""):
    #chat_id = get_chat_id(bot)
    line_list = []
    verbose = args['verbose']
    if verbose: print(args)
    try:
        for line in sys.stdin:
            line_list = textwrap.fill(line,256).split('\n') 
            if line != "":
                try:
                    new_chat_id = get_chat_id(bot)
                    chat_id = new_chat_id
                except:
                    if verbose:print("Error getting the chat_id, using {} from config file".format(chat_id))
                    pass
                if verbose:
                    print("Sending: {}".format( str(line) ) )
                if args['markdown']:
                    line = """`{}`""".format(line)
                if args['filter'] != False:
                    if verbose:
                        print("Using filter: '{}'...".format(args['filter']))
                    if args['filter'] in line:
                        bot.send_message(chat_id=chat_id, text=str(
                            line), parse_mode=telegram.ParseMode.MARKDOWN)
                    continue
                bot.send_message(chat_id=chat_id, text=str(
                    line), parse_mode=telegram.ParseMode.MARKDOWN)
    except KeyboardInterrupt:
        print("Exiting...")
        exit(0)
    #for line in line_list:
    #    if line != "":
    #        bot.send_message(chat_id = chat_id, text = str(line))
    return True


def send_message_default(bot, args, chat_id = ""):
    verbose = args['verbose']
    
    if verbose: print(args)
    whole_message = ""
    if args['markdown']:
        whole_message = "```\n"
    # Get the chat id
    try:
        new_chat_id = get_chat_id(bot)
        chat_id = new_chat_id
    except Exception as e:
        if verbose: print("Error getting the chat_id, using {} from config file".format(chat_id))
        pass
    try:
        for line in sys.stdin:
            whole_message += line
    except Exception as e:
        whole_message = "Error with {}".format(e)
        print(whole_message)
        return False
    if args['markdown']:
        whole_message += "\n```"
    if verbose:
        print("Sending the following message: \n{}".format(whole_message))
    bot.send_message(chat_id = chat_id,text = whole_message, parse_mode=telegram.ParseMode.MARKDOWN)
    return True
    

def write_chatid_2config(chat_id, config, path):
    config['DEFAULT']['saved_chat_id'] = str(chat_id)
    with open(path, "w") as a:
        config.write(a)
    return 1

if __name__ == "__main__":
    args = check_args()
    config = configparser.ConfigParser()
    config_location = str(Path.home()) + "/.SIO.conf"
    print(config)
    if args['config'] != None:
        config_location = args['config']
    config.read(config_location)
    if args['verbose'] == True: print("Reading the config from {}".format(config_location))
    if args['verbose'] == True: print(args)
    # Get the config and api key
    bot_api_key = config['DEFAULT']['apikey']
    if args['verbose'] == True: print("using Api key {}".format(bot_api_key))
    # Check if exist a chat_id to dont over ask for it
    # get the chat_id
    bot = telegram.Bot(token=str(bot_api_key))
    chat_id = 0
    try:
        chat_id = config['DEFAULT']['saved_chat_id']
        print("Chat id fetched from the config file: {} ".format(chat_id))
    except:
        if args['verbose']: print("there's not a saved chat_id, getting one and writing it down")
    if chat_id == 0:
        chat_id = get_chat_id(bot)
        write_chatid_2config(chat_id, config, config_location)
        if args['verbose']: print("Chat id saved on config file!")


    if args['follow']:
        send_message_follow(bot, args, chat_id)
        sys.exit(0)
    
    elif not args['follow'] and args['infile'] == None:
        send_message_default(bot, args, chat_id)
        sys.exit(0)

    send_message_byfile(bot,args['infile'],chat_id)



