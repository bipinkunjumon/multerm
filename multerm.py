#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2023 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the"Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED"AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import pty
import sys
import threading
import argparse
import json
from select import select

sys.path.append(os.path.join(sys.path[0],'..'))
import TermTk as ttk
from TermTk import TTkWindow, TTkColor, TTkColorGradient, TTkRadioButton, TTkSpacer
from TermTk import TTkTheme, TTkK, TTkSplitter, TTkTabWidget, TTkKodeTab
from TermTk import TTk, TTkLog, TTkHelper
from TermTk import TTkGridLayout, TTkFileTree, TTkWidget, TTkFrame

parser = argparse.ArgumentParser()
parser.add_argument('-d',  help='Debug (Add LogViewer Panel)',    action='store_true')

args = parser.parse_args()
max_window=6

  

# ttk.TTkLog.use_default_file_logging()
root = ttk.TTk(layout=ttk.TTkGridLayout())

split = ttk.TTkSplitter(parent=root, orientation=ttk.TTkK.VERTICAL)

split.addItem(top := ttk.TTkLayout())



if args.d:
    split.addWidget(ttk.TTkLogViewer(follow=False ), title='Log', size=20)

f = open('terminal.json')
data = json.load(f)
print("[***] Sessions list")
for i in data['Sessions']:
    print(i["Terminal"],i["CMD"])
print("[***] -------------[****]")

quitBtn = ttk.TTkButton(pos=(100,0),text="QUIT", border=True)
quitBtn.clicked.connect(ttk.TTkHelper.quit)

cb_c = ttk.TTkCheckbox(pos=(20,1),size=(20,1), text="CTRL-C (VINTR) ", checked=ttk.TTkK.Checked)
cb_s = ttk.TTkCheckbox(pos=(40,1),size=(20,1), text="CTRL-S (VSTOP) ", checked=ttk.TTkK.Checked)
cb_z = ttk.TTkCheckbox(pos=(60,1),size=(20,1), text="CTRL-Z (VSUSP) ", checked=ttk.TTkK.Checked)
cb_q = ttk.TTkCheckbox(pos=(80,1),size=(20,1), text="CTRL-Q (VSTART)", checked=ttk.TTkK.Checked)

cb_c.stateChanged.connect(lambda x: ttk.TTkTerm.setSigmask(ttk.TTkTerm.Sigmask.CTRL_C,x==ttk.TTkK.Checked))
cb_s.stateChanged.connect(lambda x: ttk.TTkTerm.setSigmask(ttk.TTkTerm.Sigmask.CTRL_S,x==ttk.TTkK.Checked))
cb_z.stateChanged.connect(lambda x: ttk.TTkTerm.setSigmask(ttk.TTkTerm.Sigmask.CTRL_Z,x==ttk.TTkK.Checked))
cb_q.stateChanged.connect(lambda x: ttk.TTkTerm.setSigmask(ttk.TTkTerm.Sigmask.CTRL_Q,x==ttk.TTkK.Checked))
win=["win1","win2","win3","win4","win5","win6","win7","win8","win9","win10"]
term=["term1","term2","term3","term4","term5","term6","term7","term8","term9","term10"]
th=["th1","th2","th3","th4","th5","th6","th7","th8","th9","th10"]

index=1
top.addWidgets([quitBtn, cb_c, cb_s, cb_z, cb_q])
for i in data['Sessions']:
    win[index]  = ttk.TTkWindow(pos=(20,10+index), size=(80,25), title=i["Terminal"], border=True, layout=ttk.TTkVBoxLayout(), flags = ttk.TTkK.WindowFlag.WindowMinMaxButtonsHint)
    term[index] = ttk.TTkTerminal(parent=win[index])
    th[index] = ttk.TTkTerminalHelper(term=term[index])
    th[index].runShell()
    top.addWidgets([win[index]])
    index=index+1
   

term[2].setFocus()

root.mainloop()