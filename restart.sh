cd appMain
nohup python3 manage.py runserver 0.0.0.0:8088 &
cd ../styleTransfer
nohup python3 ./code/run.py ./model/model.pth continued > ../transfer.log &