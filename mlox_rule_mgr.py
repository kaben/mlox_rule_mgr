# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 17:45:55 2021

@author: Morrowind
"""

import argparse, sys

def parse_args():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    print("hello, world.")
    print(f"args: {args}")
    
if __name__ == "__main__":
    sys.exit(main())