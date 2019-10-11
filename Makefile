test:
	pytest
deploy : test
	rsync -a --exclude-from '.gitignore' . pi@bruezpi:/home/pi/tarnow
run:
	python -m tarnow server
reboot:
	ssh pi@bruezpi sudo reboot
serve:
	gunicorn --bind 0.0.0.0:8080 tarnow:app
