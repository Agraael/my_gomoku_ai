#!/usr/bin/python3
import os

os.system("pip install pyinstaller")
os.system("pip3 install pyinstaller")
os.system("pyinstaller --onefile decision.py heuristic.py gomoku.py pisqpipe.py --name pbrain-PARIS−LELEU.HUBERT --distpath .")
