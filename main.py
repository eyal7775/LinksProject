"""
    interpeter requirement:
    - the project run on python 3.10
    recommended command:
    - python -m pip install --upgrade pip
    requirements running:
    - python -m pip install requests
    - python -m pip install progressbar2
    - python -m pip install pyyaml
    or:
    - python -m pip install -r requirements.txt
    cmd line running:
    - python <user_path>/LinksProject/main.py -r <root> -d <depth> -f <format>
"""
from formats.DBFormat import DBFormat
from formats.JsonFormat import JsonFormat
from formats.YmlFormat import YmlFormat
from formats.CSVFormat import CSVFormat
from formats.XMLFormat import XMLFormat
import argparse
import datetime

def get_user_arguments():
    # user input
    parser = argparse.ArgumentParser(description='enter root link with max depth for scanning')
    parser.add_argument('-r', '--root', help="main page from start scan", type=str, required=True)
    parser.add_argument('-d', '--depth', help="max depth for scanning", type=int, required=True)
    parser.add_argument('-f', '--format', help="file result format for display", type=str, required=True)
    # get initial arguments
    args = vars(parser.parse_args())
    return args['root'] ,args['depth'] ,args['format']

# main test
if __name__ == "__main__":
    start = datetime.datetime.now()
    root ,max_depth ,format = get_user_arguments()
    try:
        instance = None
        # check which type format by user choice
        if format == 'json':
            instance = JsonFormat(root, max_depth).run_progress()
        elif format == 'yaml' or format == 'yml':
            instance = YmlFormat(root, max_depth).run_progress()
        elif format == 'db':
            instance = DBFormat(root, max_depth).run_progress()
        elif format == 'csv':
            instance = CSVFormat(root, max_depth).run_progress()
        elif format == 'xml':
            instance = XMLFormat(root, max_depth).run_progress()
        else:
            raise Exception(str(format) + " is invalid format")
    except Exception as error:
        print(error.args[0])
    end = datetime.datetime.now()
    print("\nrun time: " + str(end - start))
    # in this case: python C:/Users/eyal999/PycharmProjects/LinksProject/main.py -r <root> -d <depth> -f <format>
