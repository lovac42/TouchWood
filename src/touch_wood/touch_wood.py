# -*- coding: utf-8 -*-
# Copyright: (C) 2019-2020 Lovac42
# Support: https://github.com/lovac42/TouchWood
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html



import aqt
from aqt import mw
from anki.hooks import wrap
from anki.utils import ids2str
from anki.lang import _
from aqt.qt import *

from anki import version
ANKI21 = version.startswith("2.1.")
if ANKI21:
    from PyQt5 import QtCore, QtGui, QtWidgets
else:
    from PyQt4 import QtCore, QtGui as QtWidgets


def getNewCardCnt(dids):
    "count new or burried only, no suspended"
    cnt=mw.col.db.first("""
Select count() from cards where
type = 0 and queue in (0,-2,-3)
and did in %s"""%ids2str(dids))[0]
    return cnt or 0


def valuechange(self):
    npd=self.newPerDay.value()
    cur=mw.col.decks.current()['id']
    kids=[did for (name, did) in mw.col.decks.children(cur)]
    dids=[cur]+kids

    tot=getNewCardCnt(dids)
    days=tot/(npd or 1)
    if tot<=0:
        msg="(Touch Wood!)"
    elif npd<1:
        msg="(inf days, %d total)"%tot
    else:
        c='s' if days>1 else ''
        msg="(%d day%s to go, %d total)"%(days or 1,c,tot)
    self.touchWoodLabel.setText(_(" "*45+msg))


def dconfsetupUi(self, Dialog):
    self.newPerDay.valueChanged.connect(lambda:valuechange(self))
    self.touchWoodLabel=QtWidgets.QLabel(self.tab)
    self.gridLayout.addWidget(self.touchWoodLabel,2,2,1,1)

aqt.forms.dconf.Ui_Dialog.setupUi = wrap(aqt.forms.dconf.Ui_Dialog.setupUi, dconfsetupUi, pos="after")
