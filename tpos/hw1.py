#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import argparse
import libtmux
import socket
import secrets
import os
from tqdm import tqdm


IP = socket.gethostbyname(socket.gethostname())


def start(args):
    """
    Запустить $num_users ноутбуков. У каждого рабочая директория $base_dir+$folder_num
    """
    server = libtmux.Server()
    session_name = args.session_name

    # Проверяем, существует ли сессия, если нет, то создать
    if not server.has_session(session_name):
        server.new_session(session_name=session_name)

    session = server.find_where({ "session_name": session_name})
    
    if args.isOne:
        path = os.path.join(args.base_dir, str(args.num_users))
        if not os.path.exists(path):
            os.makedirs(path)
        
        window_name = session_name + str(args.num_users)

        # Если такое существуют
        if window_name in str(session.windows):
            print("This window name is exist")
            return
            
        window = session.new_window(attach=False, window_name=window_name)
        pane = window.select_pane(0)
        # Запускаем Jupyter Notebook
        pane.send_keys("jupyter-notebook --ip {IP} --port {port} --no-browser --NotebookApp.token={token} --NotebookApp.notebook_dir={path}".format(
            IP=IP, port=args.port, token=args.token, path=path
            ),
            enter=True)
        print("Token for notebook:", args.token)
        
        return

    for i in tqdm(range(args.num_users)):
        
        path = os.path.join(args.base_dir, str(i))
        if not os.path.exists(path):
            os.makedirs(path)
        
        # Название окна
        window_name = session_name + str(i)

        # Если такие существуют, удалить прошлые
        if window_name in str(session.windows):
            session.kill_window(window_name)
        
        # Создаем новое окно и подключаемся к pane (фрейму) 
        window = session.new_window(attach=False, window_name=window_name)
        pane = window.select_pane(0)
        # Запускаем Jupyter Notebook
        token = secrets.token_hex()
        pane.send_keys("jupyter-notebook --ip {IP} --port {port} --no-browser --NotebookApp.token={token} --NotebookApp.notebook_dir={path}".format(
            IP=IP, port=args.port, token=token, path=path
            ),
            enter=True)
        print(f"Token for notebook's {window_name}: {token}")
        
    
    print("Done")
    print(f"Started {args.num_users} notebooks")

    

def stop(args):
    """
    @:param session_name: Названия tmux-сессии, в которой запущены окружения
    @:param num: номер окружения, кот. можно убить
    """
    server = libtmux.Server()
    session_name = args.session_name
    num = args.num
    # Находим сессию и убиваем нужное окно
    session = server.find_where({ "session_name": session_name})
    session.kill_window(session_name + num)
    print("Done")
    print(f"In session {session_name}, window {num} was killed")


def stop_all(args):
    """
    @:param session_name: Названия tmux-сессии, в которой запущены окружения
    """
    # Убиваем всю сессию 
    server = libtmux.Server()
    server.kill_session(args.session_name)
    print("Done")
    print(f"Session {args.session_name} was killed")

def msg(name=None):                                                            
    return '''hw1.py
        [start --num-users --port --token --base-dir --session_name --isOne]
        [stop --session_name --num]
        [stop-all --session_name]
        '''
    
def parse_args():
    '''Настройка argparse'''
    parser = argparse.ArgumentParser(description='Script for start or stop session in tmux', usage=msg())
    subparsers = parser.add_subparsers()
    parser_start = subparsers.add_parser('start', help='Start jupyter notebooks')
    parser_start.add_argument('--num-users', action="store", dest="num_users", default=1, type=int, help="Number of users. From 0 to num_users-1")
    parser_start.add_argument('--port', action="store", dest="port", default=8888, type=int, help="The first port of Jupyter Notebook")
    parser_start.add_argument('--token', action="store", dest="token", default=secrets.token_hex(), type=str, help="Token for Jupyter Notebook")
    parser_start.add_argument('--base-dir', action="store", dest="base_dir", default='./', type=str, help="The main directory")
    parser_start.add_argument('--session_name', action="store", dest="session_name", default='jupyter_session', type=str, help="Session name in tmux")
    parser_start.add_argument('--isOne', action="store", dest="isOne", default=False, type=bool, help="Create certain notebook")
    parser_start.set_defaults(func=start)

    parser_stop = subparsers.add_parser('stop', help='Stop a definite notebook')
    parser_stop.add_argument('--session_name', action="store", dest="session_name", default='jupyter_session', type=str, help="Session name in tmux")
    parser_stop.add_argument('--num', action="store", dest="num", default='0', type=str, help="Window number in the session")
    parser_stop.set_defaults(func=stop)

    parser_stop_all = subparsers.add_parser('stop-all', help='Stop the entire session')
    parser_stop_all.add_argument('--session_name', action="store", dest="session_name", default='jupyter_session', type=str, help="Session name in tmux")
    parser_stop_all.set_defaults(func=stop_all)

    return parser, parser.parse_args()

if __name__ == "__main__":
    parser, args = parse_args()
    if not vars(args):
        print(parser.print_help())
    else:
        args.func(args)