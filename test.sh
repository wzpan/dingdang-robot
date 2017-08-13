flake8 --exclude=wxbot.py,snowboydetect.py,client/mic_array,client/drivers dingdang.py client
nosetests -s --exe -v --with-coverage --cover-erase
