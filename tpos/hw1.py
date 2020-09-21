#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import argparse
import libtmux
import socket
from tqdm import tqdm
import os

IP = socket.gethostbyname(socket.gethostname())


def start(num_users, port, session_name, token="", base_dir='./', isOne=False):
    """
    Запустить $num_users ноутбуков. У каждого рабочая директория $base_dir+$folder_num
    """
    server = libtmux.Server()
    session = server.find_where({ "session_name": session_name})
    
    if isOne:
        path = os.path.join(base_dir, str(num_users))
        if not os.path.exists(path):
            os.makedirs(path)
        
        window_name = session_name + str(num_users)

        # Если такое существуют
        if window_name in str(session.windows):
            print("This window name is exist")
            return
            
        window = session.new_window(attach=False, window_name=window_name)
        pane = window.select_pane(0)
        # Запускаем Jupyter Notebook
        pane.send_keys("jupyter-notebook --ip {IP} --port {port} --no-browser --NotebookApp.token={token} --NotebookApp.notebook_dir={path}".format(
            IP=IP, port=port, token=token, path=path
            ),
            enter=True)
        
        return

    for i in tqdm(range(num_users)):
        
        path = os.path.join(base_dir, str(i))
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
        pane.send_keys("jupyter-notebook --ip {IP} --port {port} --no-browser --NotebookApp.token={token} --NotebookApp.notebook_dir={path}".format(
            IP=IP, port=port, token=token, path=path
            ),
            enter=True)
    
    print("Done")
    print(f"Started {num_users} notebooks")

    

def stop(session_name, num):
    """
    @:param session_name: Названия tmux-сессии, в которой запущены окружения
    @:param num: номер окружения, кот. можно убить
    """
    server = libtmux.Server()
    # Находим сессию и убиваем нужное окно
    session = server.find_where({ "session_name": session_name})
    session.kill_window(session_name + num)
    print("Done")
    print(f"In session {session_name}, window {num} was killed")


def stop_all(session_name):
    """
    @:param session_name: Названия tmux-сессии, в которой запущены окружения
    """
    # Убиваем всю сессию 
    server = libtmux.Server()
    server.kill_session(session_name)
    print("Done")
    print(f"Session {session_name} was killed")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Script for start or stop session in tmux')

    FUNCTION_MAP = {'start' : start,
                    'stop' : stop,
                    'stop-all': stop_all}

    # Select a required command for the script
    parser.add_argument('command', choices=FUNCTION_MAP.keys(), help="Actions in tmux")
    
    parser.add_argument('--num-users', action="store", dest="num_users", default=1, type=int, help="Number of users. From 0 to num_users-1")
    parser.add_argument('--port', action="store", dest="port", default=8888, type=int, help="The first port of Jupyter Notebook")
    parser.add_argument('--token', action="store", dest="token", default="", type=str, help="Token for Jupyter Notebook")
    parser.add_argument('--base-dir', action="store", dest="base_dir", default='./', type=str, help="The main directory")
    parser.add_argument('--session_name', action="store", dest="session_name", default='jupyter_session', type=str, help="Session name in tmux")
    parser.add_argument('--num', action="store", dest="num", default='0', type=str, help="Window number in the session")
    parser.add_argument('--isOne', action="store", dest="isOne", default=False, type=bool, help="Create certain notebook")
    
    args = parser.parse_args()

    func = FUNCTION_MAP[args.command]

    if func == start:
       start(num_users=args.num_users, port=args.port, session_name=args.session_name, token=args.token, base_dir=args.base_dir, isOne=args.isOne)
    elif func == stop:
        stop(session_name=args.session_name, num=args.num)
    elif func == stop_all:
        stop_all(session_name=args.session_name)