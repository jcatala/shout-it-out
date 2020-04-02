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
    parser.add_argument('-f', '--file',help="Send a text file (default is stdin)")
    parser.add_argument('-v', '--verbose',required = False, help="Turn on the verbose mode", action="store_true",default=False)
    parser.add_argument('-F', '--filter',required = False, help="Add a filter before sending the message (string: default: None)",default=False)
    return vars(parser.parse_args())


def get_chat_id(bot):
    chat_id = bot.get_updates()[-1]['message']['chat']['id']
    return chat_id


def send_message_byfile(bot, file_name):
    chat_id = get_chat_id(bot)
    with open(file_name, "r") as a:
        content = a.read().strip('\n')
    payload = textwrap.fill(content,256).split('\n')
    for k in payload:
        if k != "":
            bot.send_message(chat_id = chat_id, text = str(k))
    return True

def send_message_default(bot,args):
    #chat_id = get_chat_id(bot)
    line_list = []
    verbose = args['verbose']
    if verbose: print(args)
    chat_id = ""
    try:
        for line in sys.stdin:
            line_list = textwrap.fill(line,256).split('\n') 
            if line != "":
                try:
                    new_chat_id = get_chat_id(bot)
                    chat_id = new_chat_id
                except:
                    if verbose:print("Error getting the chat_id")
                    pass
                if verbose:
                    print("Sending: {}".format( str(line) ) )
                if args['filter'] != False:
                    if verbose:
                        print("Using filter: '{}'...".format(args['filter']))
                    if args['filter'] in line:
                        bot.send_message(chat_id = chat_id, text = str(line))
                    continue
                bot.send_message(chat_id = chat_id, text = str(line))
    except KeyboardInterrupt:
        print("Exiting...")
        exit(0)
    #for line in line_list:
    #    if line != "":
    #        bot.send_message(chat_id = chat_id, text = str(line))
    return True


if __name__ == "__main__":
    args = check_args()
    config = configparser.ConfigParser()
    config_location = str(Path.home()) + "/.SIO.conf"
    print(config)
    if args['config'] != None:
        config_location = args['config']
    config.read(config_location)
    if args['verbose'] == True: print("Reading the config from {}".format(config_location))
    # Get the config and api key
    bot_api_key = config['DEFAULT']['apikey']
    if args['verbose'] == True: print("using Api key {}".format(bot_api_key))

    # get the chat_id
    bot = telegram.Bot(token = str(bot_api_key))

    if args['file'] == None:
        send_message_default(bot,args)
        exit(0)
    send_message_byfile(bot,args['file'])



