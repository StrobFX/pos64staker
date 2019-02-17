#!/usr/bin/env python3

from slickrpc import Proxy
import json
import sys
import os
import stakerlib

def load_conf():
    try:
        with open('staker.conf') as file:
            staker_conf = json.load(file)
    except Exception as e:
        print(e)
        staker_conf = []
        user_input = input('No staker.conf conf file, specify a chain to begin:')
        staker_conf.append([user_input])
        with open('staker.conf', "a+") as f:
            json.dump(staker_conf, f)
    return(staker_conf)

def initial_menu(staker_conf, error):
    os.system('clear')
    print(stakerlib.colorize(error, 'red'))
    print(stakerlib.colorize('pos64staker by KMDLabs', 'green'))
    print(stakerlib.colorize('===============', 'blue'))
    menu_item = 0
    for i in staker_conf:
        print(str(menu_item) + ' | ' + str(i[0]))
        menu_item += 1
    print('\n' + str(len(staker_conf)) + ' | Start a chain from assetchains.json')
    print(str(len(staker_conf) + 1) + ' | <Add/remove chain>')
    print('q | Exit TUI')
    print(stakerlib.colorize('===============\n', 'blue'))

def print_menu(menu_list, chain, msg):
    if msg[:5] == 'Error':
        print(stakerlib.colorize(msg, 'red'))
    else:
        print(stakerlib.colorize(msg, 'green'))
    print(stakerlib.colorize('\n' + chain, 'magenta'))
    print(stakerlib.colorize('===============', 'blue'))
    print('0 | <return to previous menu>\n')
    menu_item = 1
    for i in menu_list:
        print(str(menu_item) + ' | ' + str(i))
        menu_item += 1
    print('\nq | Exit TUI')
    print(stakerlib.colorize('===============\n', 'blue'))


def add_chain(chain):
    staker_conf = load_conf()
    if chain == 0:
        new_chain = input('Add/remove chain:')
    else:
        new_chain = chain
    # delete and restart loop if user inputted chain exists in conf
    for i in (range(len(staker_conf))):
        if staker_conf[i][0] ==  new_chain:
            del staker_conf[i]
            with open('staker.conf', mode='w', encoding='utf-8') as f:
                json.dump(staker_conf, f)
            select_loop('')
    # add new chain to conf, stored as a list in case we want to save something, dummy value for now
    staker_conf.append([new_chain, 1])
    with open('staker.conf', mode='w', encoding='utf-8') as f:
        json.dump(staker_conf, f)
    return(0)


def select_loop(error):
    staker_conf = load_conf()
    initial_menu(staker_conf, error)
    chain_index = stakerlib.user_inputInt(0,len(staker_conf) + 1,"Select chain:")
    while True:
        # Start chain from assetchains.json
        if chain_index == len(staker_conf):
            user_chain = input('Please specify chain. It must be defined in assetchains.json. ' +
                               'If assetchains.json does not exist locally, the official one ' +
                               'will be fetched from jl777\'s repo.\nChain: ')
            stakerlib.start_daemon(user_chain)
            add_chain(user_chain)
            chain_loop(user_chain, '')
        # add/remove chain
        elif chain_index == len(staker_conf) + 1:
            add_chain(0)
            staker_conf = load_conf()
            initial_menu(staker_conf, '')
            chain_index = stakerlib.user_inputInt(0,len(staker_conf) + 1,"Select chain:")
        else:
            chain = staker_conf[chain_index][0]
            chain_loop(chain, '')

# Chain menu, to add additional options, add what will be displayed to chain_menu
# and an elif for it's position in the list
def chain_loop(chain, msg):
    os.system('clear')
    try:    
        rpc_connection = stakerlib.def_credentials(chain)
        dummy = rpc_connection.getbalance() # test connection
    except:
        os.system('clear')
        error = 'Error: Could not connect to daemon. ' + chain + ' is not running or rpc creds not found.'
        select_loop(error)
    while True:
        os.system('clear')
        print_menu(chain_menu, chain, msg)
        selection = stakerlib.user_inputInt(0,len(chain_menu),"make a selection:")
        if int(selection) == 0:
            os.system('clear')
            select_loop('')
        elif int(selection) == 1:
            msg = stakerlib.sendmany64_TUI(chain, rpc_connection)
            chain_loop(chain, msg)
        elif int(selection) == 2:
            msg = stakerlib.RNDsendmany_TUI(chain, rpc_connection)
            chain_loop(chain, msg)
        elif int(selection) == 3:
            msg = stakerlib.genaddresses(chain, rpc_connection)
            chain_loop(chain, msg)
        elif int(selection) == 4:
            msg = stakerlib.import_list(chain, rpc_connection)
            chain_loop(chain, msg)
        elif int(selection) == 5:
            msg = stakerlib.withdraw_TUI(chain, rpc_connection)
            chain_loop(chain, msg)
        elif int(selection) == 6:
            msg = stakerlib.createchain(chain, rpc_connection)
            chain_loop(chain, msg)
        elif int(selection) == 7:
            msg = stakerlib.restart_daemon(chain, rpc_connection)
            chain_loop(chain, msg)
        else:
            print('BUG!')

chain_menu = ['sendmany64','RNDsendmany', 'genaddresses', 'importlist', 'withdraw', 'Start a new chain', 'Restart daemon with -blocknotify']
os.system('clear')
select_loop('')
