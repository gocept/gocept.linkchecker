# Copyright (c) 2005 gocept gmbh & co. kg
# See also LICENSE.txt
# $Id$

TARGETS=INSTALL.html HOWTO-Developers.html HOWTO-MailNotifications.html \
	TODO.html README.html
HLEVEL?=1

all: $(TARGETS)

clean:
	rm -f $(TARGETS)


%.html: %.txt
	html.py --initial-header-level=${HLEVEL} $< $@


