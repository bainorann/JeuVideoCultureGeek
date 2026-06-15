#!/usr/bin/env python3
import os
import sys

if getattr(sys, "frozen", False):
    base_dir = os.path.dirname(sys.executable)
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(base_dir)

from tests.test11 import run

if __name__ == "__main__":
    run()
