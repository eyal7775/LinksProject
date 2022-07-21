import re
import requests # pip install requests
import datetime
import json
import progressbar # pip install progressbar2
import argparse
import itertools
import yaml # pip install pyyaml
import io
# usage: python links.py -r https://www.ynet.co.il/home/0,7340,L-8,00.html -d 2 -f yaml

# user input
parser = argparse.ArgumentParser(description='enter root link with max depth for scanning')
parser.add_argument('-r', '--root', help="main page from start scan", type=str, required=True)
parser.add_argument('-d', '--depth', help="max depth for scanning", type=int, required=True)
parser.add_argument('-f', '--format', help="file result format for display", type=str, required=True)
args = vars(parser.parse_args())
root ,max_depth ,format = args['root'] ,args['depth'] ,args['format']

# global variables
serial = 1
visited = []
file_path = root.split('.')[1] + "_" + str(max_depth) + "." + format

# design for progress bar
widgets = [
    progressbar.Timer(format='elapsed time: %(elapsed)s'), ' ',
    progressbar.Bar('*'), '',
    progressbar.Percentage(), '',
]

# create custom file format by user choise
def create_file_format():
    with io.open(file_path, 'w', encoding='utf8') as file:
        if format == 'yaml' or format == 'yml':
            yaml.dump({}, file, default_flow_style=False, allow_unicode=True, sort_keys=False)
        elif format == 'json':
            json.dump({}, file, indent=4)
        else:
            raise Exception('the format is invalid')

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
        if link:
            fix_links.append(link)
    return fix_links

# create datasets information for each link
def create_datasets(links ,depth):
    datasets = []
    print("\nextract urls from " + str(root) + " in depth " + str(depth) + ":")
    bar = progressbar.ProgressBar(max_value=len(links), widgets=widgets).start()
    i = 0
    for link in links:
        if not link in visited:
            dataset = (link ,depth ,try_open_url(link))
            datasets.append(dataset)
            visited.append(link)
        bar.update(i)
        i = i + 1
    return datasets

# check access to url
def try_open_url(link):
    try:
        access = requests.get(link ,headers={'User-Agent': 'Mozilla/5.0'} ,allow_redirects=False)
        return access.status_code in [200 ,301 ,302 ,303 ,403 ,406 ,500 ,999]
    except:
        return False

# insert urls data to file results
def add_data_to_json(datasets):
    next = read_from_file()
    global serial
    for dataset in datasets:
        link ,depth ,access = dataset[0] ,dataset[1] ,dataset[2]
        key = 'url_' + str(serial)
        value = {
            "path": link,
            "depth": depth,
            "access": access
        }
        next[key] = value
        serial = serial + 1
    write_to_file(next)

# read latest data from file results
def read_from_file():
    with open(file_path , "r") as file:
        if format == 'yaml' or format == 'yml':
            content = yaml.safe_load(file)
        elif format == 'json':
            content = json.load(file)
    return content

# write new data to file results
def write_to_file(content):
    with io.open(file_path, 'w', encoding='utf8') as file:
        if format == 'yaml' or format == 'yml':
            yaml.dump(content, file, default_flow_style=False, allow_unicode=True, sort_keys=False)
        elif format == 'json':
            json.dump(content, file, indent=4)

# download all data from main url up to max depth
def download_urls(links ,depth = 0):
    if depth == max_depth:
        return links
    else:
        cumulative = []
        extracts = list(itertools.chain(*map(extract_urls, links)))
        datasets = create_datasets(extracts, depth + 1)
        cumulative = cumulative + datasets
        add_data_to_json(cumulative)
        new_links = [dataset[0] for dataset in cumulative]
        return links + download_urls(new_links ,depth + 1)

# main test
if __name__ == "__main__":
    start = datetime.datetime.now()
    create_file_format()
    access = try_open_url(root)
    first = {
        "url_0": {
            "path": root,
            "depth": 0,
            "access": access
        }
    }
    write_to_file(first)
    if access:
        visited.append(root)
        links = download_urls([root])
        assert len(set(links)) == len(links)
    end = datetime.datetime.now()
    print("\nrun time: " + str(end - start))
