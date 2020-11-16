#!/usr/bin/env python
import time
import logging


      
def main():
    #logging.basicConfig(filename='output.log', level=logging.INFO)

    while (True):
        logging.info("[I] Main: Process interrupted pressing [Ctl] + [C] keys")
        time.sleep(3)
        
main()