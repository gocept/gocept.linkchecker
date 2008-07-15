# Copyright (c) 2005 gocept gmbh & co. kg
# See also LICENSE.txt
# $Id: Makefile,v 1.2 2005/04/11 11:01:57 zagy Exp $

TARGETS=INSTALL.html HOWTO-Developers.html HOWTO-MailNotifications.html \
	TODO.html README.html
HLEVEL?=1

all: $(TARGETS)

clean:
	rm -f $(TARGETS)


%.html: %.txt
	html.py --initial-header-level=${HLEVEL} $< $@


