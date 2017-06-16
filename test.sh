flake8 --exclude=wxbot.py,snowboydetect.py dingdang.py client
nosetests -s --exe -v --with-coverage --cover-erase
