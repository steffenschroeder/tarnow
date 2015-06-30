test:
	nosetests
deploy : test
	rsync -a --exclude-from '.gitignore' . pi@192.168.0.12:/home/pi/tarnow
run:
	python tarnow.py
