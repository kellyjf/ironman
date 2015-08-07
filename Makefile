
UIFILES := swim.py

all : $(UIFILES)

%.py : %.ui
	pyuic4 --indent=0  -o $@ $<

test:
	python ./Swim.py

clean:
	rm -f $(UIFILES) *.pyc


