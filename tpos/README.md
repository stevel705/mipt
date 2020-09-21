# Home work 1

## Init
Перед запуском скрипта нужно создать новую сессию в tmux 

Например:
```
tmux new -s <name_session>
```
Где name_session - назание сессии. 

## Запуск
Скрипт выполняет три опрерации start, stop и stop_all.

### start: запуск N ноутбуков в определенной директории

Принимает параметры: num_users, port, session_name, token, base_dir, isOne.

* num_users - кол-во ноутбуков, которые нужно создать в своей директории.
* port - начальный порт, на котором будут запускаться ноутбуки. 
* session_name - название сессии, к которой необходимо подключиться 
* token - токен для подключения к ноутбуку, по умолчанию его нет 
* base_dir - основаня директория в которой будут создаваться ноутбуки для юзеров
* isOne - флаг, для указания того, что нужно создать определенное окно, где номер окна является num_users

Пример: 
```
python3 hw1.py start --session_name jupyter_session  --num-users 5 --token hello
python3 hw1.py start --num-users 100500 --isOne True
```

### stop: Выключение определенного окна
Принимает параметры: session_name, num
* session_name - название сессии, к которой необходимо подключиться 
* num - номер окна, который необходимо убить

Пример: 
```
python3 hw1.py stop --session_name jupyter_session --num 1
```

### stop_all: выключение всей сессии
Принимает параметры: session_name

* session_name - название сессии, которую необходимо убить

Пример: 
```
python3 hw1.py stop-all
```


