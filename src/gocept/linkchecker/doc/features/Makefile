# Copyright (c) 2005-2006 gocept gmbh & co. kg
# See also LICENSE.txt
# 

TARGETS=FEATURES.html
HLEVEL?=1

all: $(TARGETS)

clean:
	rm -f $(TARGETS) FEATURES_public.html

public: FEATURES_public.html
	

FEATURES_public.html: FEATURES.html
	cat FEATURES.html | \
	  sed 's/src="/src="http:\/\/images.gocept.com\/CMFLinkChecker\/features\//'\
	  > FEATURES_public.html

	

%.html: %.txt
	html.py --initial-header-level=${HLEVEL} $< $@


