
UIFILES := workout.py gear.py ironman.py summary.py

all : test

workout.sqlite : train.sql
	sqlite3 $@ < $<

save:
	sqlite3  -init savedb.sql workout.sqlite < /dev/null 

restore:
	sqlite3  workout.sqlite < save.sql 

%.py : %.ui
	pyuic4 --indent=0  -o $@ $<

test: $(UIFILES)
	python ./Workout.py

clean:
	rm -f $(UIFILES) *.pyc


