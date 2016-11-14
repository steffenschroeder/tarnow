test:
	python -m unittest discover -p "*_test.py"
deploy : test
	rsync -a --exclude-from '.gitignore' . pi@bruezpi:/home/pi/tarnow
run:
	python tarnow.py
reboot:
	ssh pi@bruezpi sudo reboot
