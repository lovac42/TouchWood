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


from .lib.com.lovac42.anki.version import ANKI21

if ANKI21:
    from PyQt5 import QtCore, QtGui, QtWidgets
else:
    from PyQt4 import QtCore, QtGui as QtWidgets



def getNewCardCnt(dids):
    "count new or burried only, no suspended"
    cnt = mw.col.db.first("""
Select count() from cards where
type=0 and queue in (0,-2,-3)
and did in %s"""%ids2str(dids))[0]
    return cnt or 0


def valuechange(dconf):
    new_per_day = dconf.newPerDay.value()
    current_deck_id = mw.col.decks.current()['id']
    child_decks_ids = [did for name,did in mw.col.decks.children(current_deck_id)]
    dids = [current_deck_id] + child_decks_ids

    tot = getNewCardCnt(dids)
    days = tot//(new_per_day or 1)
    if tot <= 0:
        msg = "(Touch Wood!)"
    elif new_per_day < 1:
        msg = "(inf days, %d total)"%tot
    else:
        c = 's' if days > 1 else ''
        msg = "(%d day%s to go, %d total)"%(days or 1, c, tot)
    dconf.touchWoodLabel.setText(" "*45+msg)


def dconfsetupUi(dconf, Dialog):
    dconf.newPerDay.valueChanged.connect(lambda:valuechange(dconf))
    dconf.touchWoodLabel = QtWidgets.QLabel(dconf.tab)
    dconf.gridLayout.addWidget(dconf.touchWoodLabel,2,2,1,1)


aqt.forms.dconf.Ui_Dialog.setupUi = wrap(
    aqt.forms.dconf.Ui_Dialog.setupUi,
    dconfsetupUi,
    pos = "after"
)
