#!/usr/bin/env python3

from slickrpc import Proxy
import json
import sys
import stakerlib

def selectRangeInt(low,high, msg):
    while True:
        user_input = input(msg)
        if user_input == ('q' or 'quit'):
            print('Exiting...')
            sys.exit(0)
        try:
            number = int(user_input)
        except ValueError:
            print("integer only, try again")
            continue
        if low <= number <= high:
            return number
        else:
            print("input outside range, try again")

def selectRangeFloat(low,high, msg):
    while True:
        try:
            number = float(user_input)
        except ValueError:
            print("integer only, try again")
            continue
        if low <= number <= high:
            return number
        else:
            print("input outside range, try again")

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

def initial_menu(staker_conf):
    print('\n===============')
    menu_item = 0
    for i in staker_conf:
        print(str(menu_item) + ' | ' + str(i[0]))
        menu_item += 1
    print('\n' + str(len(staker_conf)) + ' | <Add/remove chain>')
    print('q | Exit TUI')
    print('===============\n')

def print_menu(menu_list):
    print('\n===============')
    menu_item = 0
    for i in menu_list:
        print(str(menu_item) + ' | ' + str(i))
        menu_item += 1
    print('\n' + str(len(menu_list)) + ' | <return to previous menu>')
    print('q | Exit TUI')
    print('===============\n')

def select_loop():
    staker_conf = load_conf()
    initial_menu(staker_conf)
    chain_index = selectRangeInt(0,len(staker_conf),"Select chain:")
    while True:
        if chain_index == len(staker_conf):
            new_chain = input('Add/remove chain:')
            # delete and restart loop if user inputted chain exists in conf
            for i in (range(len(staker_conf))):
                if staker_conf[i][0] ==  new_chain:
                    del staker_conf[i]
                    with open('staker.conf', mode='w', encoding='utf-8') as f:
                        json.dump(staker_conf, f)
                    select_loop()
            # add new chain to conf, stored as a list in case we want to save something, dummy value for now
            staker_conf.append([new_chain, 1])
            with open('staker.conf', mode='w', encoding='utf-8') as f:
                json.dump(staker_conf, f)
            initial_menu(staker_conf)
            chain_index = selectRangeInt(0,len(staker_conf),"Select chain:")
        else:
            #chain_index = selectRangeInt(0,len(staker_conf),"Select chaineee:")
            chain = staker_conf[chain_index][0]
            chain_loop(chain)

# Chain menu, to add additional options, add what will be displayed to chain_menu
# and an elif for it's position in the list
def chain_loop(chain):
    try:    
        rpc_connection = stakerlib.def_credentials(chain)
        dummy = rpc_connection.getbalance() # test connection
    except:
        print('Could not connect to daemon. ' + chain + ' is not running or rpc creds not found.')
        select_loop()
    while True:
        print_menu(chain_menu)
        selection = selectRangeInt(0,len(chain_menu),"make a selection:")
        if int(selection) == len(chain_menu):
            select_loop()
        elif int(selection) == 0:
            stakerlib.sendmany64_TUI(chain, rpc_connection)
        elif int(selection) == 1:
            stakerlib.RNDsendmany_TUI(chain, rpc_connection)
        elif int(selection) == 2:
            stakerlib.genaddresses(chain, rpc_connection)
        elif int(selection) == 3:
            stakerlib.import_list(chain, rpc_connection)
        elif int(selection) == 4:
            stakerlib.withdraw_TUI(chain, rpc_connection)
        else:
            print('BUG!')

chain_menu = ['sendmany64','RNDsendmany', 'genaddresses', 'importlist', 'withdraw']
select_loop()



