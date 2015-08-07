
UIFILES := swim.py

all : $(UIFILES)

%.py : %.ui
	pyuic4 --indent=0  -o $@ $<

clean:
	rm -f $(UIFILES) *.pyc


