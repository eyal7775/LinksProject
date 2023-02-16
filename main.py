"""
    requirements running:
    - python -m pip install requests
    - python -m pip install progressbar2
    - python -m pip install pyyaml
    or:
    - python -m pip install -r requirements.txt
    cmd line running:
    - python C:/Users/<user_name>/PycharmProjects/LinksProject/main.py -r <root> -d <depth> -f <format>
"""
from formats.DBFormat import DBFormat
from formats.JsonFormat import JsonFormat
from formats.YmlFormat import YmlFormat
import argparse
import datetime
# import Rest_API

# user input
parser = argparse.ArgumentParser(description='enter root link with max depth for scanning')
parser.add_argument('-r', '--root', help="main page from start scan", type=str, required=True)
parser.add_argument('-d', '--depth', help="max depth for scanning", type=int, required=True)
parser.add_argument('-f', '--format', help="file result format for display", type=str, required=True)

# get initial arguments
args = vars(parser.parse_args())
root ,max_depth ,format = args['root'] ,args['depth'] ,args['format']

# main test
if __name__ == "__main__":
    start = datetime.datetime.now()
    instance = None
    if format == 'json':
        instance = JsonFormat(root,max_depth)
    elif format == 'yaml' or format == 'yml':
        instance = YmlFormat(root, max_depth)
    elif format == 'db':
        instance = DBFormat(root, max_depth)
    instance.run_progress()
    end = datetime.datetime.now()
    print("\nrun time: " + str(end - start))
    # Rest_API.run()
