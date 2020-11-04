### Tmux

#### Установка
```
apt install tmux
pip3 install libtmux
```

Terminal multiplexor.
* Можно запустить неск. терминалов в 1 окне,
* Если соединение с сервером рухнуло, tmux-сессия продолжит работать в фоне.
* Работает в консоли (не нужен Xorg).

##### Структура

```
server
|-- session
|-- -- window
|-- -- -- pane (область, фрейм)
```
##### Работа с tmux

* При запуске по умолчанию (команда `tmux`) стартует 1 сервер, 1 сессия, 1 окно, 1 область.
* `Ctrl+b x` - убить текущую область.
* `Ctrl+b d` (detach) - выйти из сессии (но оставить её живой). 
* `tmux a` - подключиться к сессии. `tmux a -t $name` если сессий несколько.
* `Ctrl+b "`, `Ctrl+b %` - разбить окно на сесии. 

[Доп. команды](https://thoughtbot.com/blog/a-tmux-crash-course)


##### Задание

Написать программу, которая запускает в tmux *N* изолированных окружений Jupyter.
* У каждого окружения должна быть своя рабочая директория, свой порт и токен.
* Каждое окружение должно жить в своём tmux-окне.
* Программа должна уметь стартовать и убивать окружения.
* При старте окружений должен выводиться progress bar (т.к. старт большого кол-ва сессий с Jupyter может занять время). Для этого можно использовать библиотеку tqdm.

Команда, с помощью которой можно стартовать Jupyter'ы:
```
jupyter notebook --ip {} --port {} --no-browser --NotebookApp.token='{}' --NotebookApp.notebook_dir='{}'
```

Интерфейс для реализации.

```python
import libtmux
import socket
import os
import tqdm


def start(num_users, base_dir='./'):
    """
    Запустить $num_users ноутбуков. У каждого рабочай директория $base_dir+$folder_num
    """
    pass
    

def stop(session_name, num):
    """
    @:param session_name: Названия tmux-сессии, в которой запущены окружения
    @:param num: номер окружения, кот. можно убить
    """
    pass


def stop_all(session_name):
    """
    @:param session_name: Названия tmux-сессии, в которой запущены окружения
    """
    pass

```

##### Литература
* [The Tao of Tmux](https://leanpub.com/the-tao-of-tmux/read)
* [Документация по LibTmux](https://libtmux.git-pull.com/en/latest/)