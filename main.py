# Main Entry


import argparse
import pathlib
from src.taskcore.task_utilities import *

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('task_json_file', default='./task.json')
    args = parser.parse_args()
    fp = pathlib.Path(args.task_json_file)
    fp.resolve(True)
    print(fp)
    tb = TaskBuilder(fp)
    res = tb.execute()
    print(res)

