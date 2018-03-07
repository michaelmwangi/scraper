import sys
from scraper import Scraper


if __name__ == '__main__':
    args = sys.argv
    maxloops = 1

    if len(args) > 1:
        if len(args) == 3:
            cmd = args[1]

            if cmd != "allowloops":
                print("Expected command is allowloops but got {} instead".format(cmd))
                exit(1)
            try:
                maxloops = int(args[2])
            except ValueError as exc:
                print("Expected an integer for number of looops allowed ")
                exit(1)
        else:
            print("Usage is python main.py cmd numberofloops")    
            exit(1)
            
    scraper = Scraper(map_url='https://s3-eu-west-1.amazonaws.com/legalstart/thumbscraper_input_tampered.hiring-env.json', max_loops=maxloops)
    scraper.scrap()