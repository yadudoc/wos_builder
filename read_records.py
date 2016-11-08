#!/usr/bin/env python

def get_record(filehandle):
    record = ''
    flag   = False
    for line in filehandle:
        if flag != True and not line.startswith('<REC'):
            continue;
        flag = True

        record = record + line
        
        if line.strip().endswith('</REC>'):
            return record

    return None

if __name__ == "__main__":
    import argparse
    
    parser   = argparse.ArgumentParser()
    parser.add_argument("-s", "--sourcefile", default="sample.xml", help="Path to data file")
    parser.add_argument("-v", "--verbosity", default="DEBUG", help="set level of verbosity, DEBUG, INFO, WARN")
    parser.add_argument("-l", "--logfile", default="./extract.log", help="Logfile path. Defaults to ./tabulator.log")

    args   = parser.parse_args()

    count = 0
    with open(args.sourcefile, 'r') as data:

        while True:
            count += 1
            test = get_record(data)
            if not test:
                break

            print "*"*50
            print test
            print "*"*20, count, "*"*30
            break

    
        
