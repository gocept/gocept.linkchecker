##############################################################################
#
# Copyright (c) 2003 gocept gmbh & co. kg. All rights reserved.
#
# See also LICENSE.txt
#
##############################################################################
"""Customized HTML parser to find images in an imglist (similar to anchorlist)

$Id: lchtmllib.py,v 1.2 2004/01/22 17:27:48 ctheune Exp $"""
from htmllib import HTMLParser

class LCHTMLParser(HTMLParser):

    imglist = []

    def do_img(self, attrs):
        for attrname, value in attrs:
            if attrname == "src":
                if not self.imglist:
                    self.imglist = []
                self.imglist.append(value)
