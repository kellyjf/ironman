
UIFILES := workout.py gear.py ironman.py

all : test

workout.sqlite : train.sql
	sqlite3 $@ < $<

%.py : %.ui
	pyuic4 --indent=0  -o $@ $<

test: $(UIFILES)
	python ./Workout.py

clean:
	rm -f $(UIFILES) *.pyc


