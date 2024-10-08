all:
	python3 main.py

requirements:
	pip install --upgrade --requirement requirements.txt

clean:
	rm events.csv

.PHONY: all clean
