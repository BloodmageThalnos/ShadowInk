cd .\appMain
del /q .\log\*.log
start cmd /c python manage.py runserver
cd ..\styleTransfer\
start cmd /c python .\code\run.py .\model\model.pth continued .\test\input\ .\test\output\

