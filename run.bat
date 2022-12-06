@echo off

title HIKKA

:RUN
cls
echo Hikka is starting...
python -m hikka
timeout /T 3
goto RUN
