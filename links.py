import re
import requests # pip install requests
import datetime
import json
import progressbar # pip install progressbar2
import argparse
import yaml # pip install pyyaml
import io
import sqlite3
# usage: python links.py -r https://edition.cnn.com -d 2 -f yml

# user input
parser = argparse.ArgumentParser(description='enter root link with max depth for scanning')
parser.add_argument('-r', '--root', help="main page from start scan", type=str, required=True)
parser.add_argument('-d', '--depth', help="max depth for scanning", type=int, required=True)
parser.add_argument('-f', '--format', help="file result format for display", type=str, required=True)
# parser.add_argument('-s', '--search', help="get links by search words", type=str, required=False)

# get initial arguments
args = vars(parser.parse_args())
root ,max_depth ,format = args['root'] ,args['depth'] ,args['format']
timestamp = datetime.datetime.now().strftime('%m-%d-%Y %H-%M-%S')
datasets = []

# global variables
serial = 0
visited = []
file_path = root.split('.')[1] + "_md" + str(max_depth) + "_" + timestamp + "." + format
ignore = ['ico','css','js','png','jpg','xml','json','svg','woff2','doc','aspx','pdf','io','php']

# design for progress bar
widgets = [
    progressbar.Timer(format='elapsed time: %(elapsed)s'), ' ',
    progressbar.Bar('*'), '',
    progressbar.Percentage(), '',
]

# create custom file format by user choice
def create_file_format():
    with io.open(file_path, "w", encoding='utf8') as file:
        if format == 'yaml' or format == 'yml':
            yaml.dump({}, file, default_flow_style=False, allow_unicode=True, sort_keys=False)
        elif format == 'json':
            json.dump({}, file, indent=4)
        else:
            raise Exception('the format is invalid')

# insert url data to file results if exist
def add_data_to_file(link ,depth):
    dataset = create_dataset(link ,depth)
    datasets.append(dataset)
    if dataset:
        data = read_from_file()
        global serial
        link, depth, access = dataset[1], dataset[2], dataset[3]
        key = 'url_' + str(serial)
        value = {
            "link": link,
            "depth": depth,
            "access": access,
        }
        data[key] = value
        serial = serial + 1
        write_to_file(data)

# create dataset information for link
def create_dataset(link ,depth):
    dataset = []
    global serial
    if not link in visited:
        dataset = (serial, link, depth, try_open_url(link))
        visited.append(link)
    return dataset

# check access to url
def try_open_url(link):
    try:
        access = requests.get(link ,headers={'User-Agent': 'Mozilla/5.0'} ,allow_redirects=False)
        return access.status_code in [200 ,301 ,302 ,303 ,403 ,406 ,500 ,999]
    except:
        return False

# read latest data from file results
def read_from_file():
    with open(file_path , "r") as file:
        if format == 'yaml' or format == 'yml':
            data = yaml.safe_load(file)
        elif format == 'json':
            data = json.load(file)
    return data

# write new data to file results
def write_to_file(data):
    with io.open(file_path, "w", encoding='utf8') as file:
        if format == 'yaml' or format == 'yml':
            yaml.dump(data, file, default_flow_style=False, allow_unicode=True, sort_keys=False)
        elif format == 'json':
            json.dump(data, file, indent=4)

# extract urls set from general url
def extract_urls(link):
    try:
        response = requests.get(link ,headers={'User-Agent': 'Mozilla/5.0'} ,allow_redirects=False)
        html = response.content.decode('latin1')
        extracts = re.findall('href="[https:]*[/{1,2}#]*[\w+.\-/=?_#]*"' ,html)
        fix_links = fix_urls([link.replace('href=', '').replace('"', '') for link in extracts])
        return fix_links
    except:
        return []

# try open url and response html content
def try_get_html(link):
    try:
        response = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'}, allow_redirects=False)
        html = response.content.decode('latin1')
        return html
    except:
        return ''

# fix incomplete urls to access active
def fix_urls(links):
    fix_links = []
    for link in links:
        if '?' in link:
            link = link[:link.find('?')]
        if '#' in link:
            link = link[:link.find('#')]
        if link.startswith('//'):
            link = 'https:' + link
        elif link.startswith('/') and len(link) > 1:
            link = 'https://' + root.split('/')[2] + link
        elif not '/' in link:
            link = 'https://' + root.split('/')[2] + '/' + link
        link = link[:-1] if link.endswith('/') else link
        if link and not link in visited:
            fix_links.append(link)
    return fix_links

# download all data from main url up to max depth
def download_urls(links ,depth = 0):
    if depth > max_depth:
        return []
    else:
        print("\nextract urls from " + str(root) + " in depth " + str(depth) + ":")
        bar = progressbar.ProgressBar(max_value=len(links), widgets=widgets).start()
        next = 0
        cumulative = []
        for link in links:
            if not link.split('.')[-1] in ignore:
                add_data_to_file(link ,depth)
                extracts = list(set(extract_urls(link)))
                cumulative = cumulative + extracts
            bar.update(next)
            next = next + 1
        return links + download_urls(cumulative ,depth + 1)

# main test
if __name__ == "__main__":
    start = datetime.datetime.now()
    create_file_format()
    links = download_urls([root])
    assert len(set(links)) == len(links)
    end = datetime.datetime.now()
    print("\nrun time: " + str(end - start))

# git checkout dev1
# git checkout origin/master
# git push origin master
# ctrl + k
