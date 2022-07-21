import re
import requests # pip install requests
import datetime
import json
import progressbar # pip install progressbar2
import argparse
# usage: python links.py -r https://www.ynet.co.il/home/0,7340,L-8,00.html -d 2

# user input
parser = argparse.ArgumentParser(description='enter root link with max depth for scanning')
parser.add_argument('-r', '--root', help="main page from start scan", type=str, required=True)
parser.add_argument('-d', '--depth', help="max depth for scanning", type=int, required=True)
args = vars(parser.parse_args())
root = args['root']
max_depth = args['depth']

# global variables
serial = 1
visited = []
json_path = root.split('.')[1] + "_" + str(max_depth) + ".json"

# design for progress bar
widgets = [
    progressbar.Timer(format='elapsed time: %(elapsed)s'), ' ',
    progressbar.Bar('*'), '',
    progressbar.Percentage(), '',
]

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
    for link in links:
        if not link in visited:
            dataset = (link ,depth ,try_open_url(link))
            datasets.append(dataset)
            visited.append(link)
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
    with open(json_path ,"r") as file:
        result = json.load(file)
    global serial
    for dataset in datasets:
        link ,depth ,access = dataset[0] ,dataset[1] ,dataset[2]
        key = 'url_' + str(serial)
        value = {
            "path": link,
            "depth": depth,
            "access": access
        }
        result[key] = value
        serial = serial + 1
    with open(json_path ,"w") as file:
        json.dump(result ,file ,indent=4)

# download all data from main url up to max depth
def download_urls(links ,depth = 0):
    if depth == max_depth:
        return links
    else:
        print("\nextract urls from " + str(root) + " in depth " + str(depth + 1) + ":")
        bar = progressbar.ProgressBar(max_value=len(links) ,widgets=widgets).start()
        i = 0
        cumulative = []
        for link in links:
            extracts = extract_urls(link)
            datasets = create_datasets(extracts ,depth + 1)
            cumulative = cumulative + datasets
            bar.update(i)
            i = i + 1
        add_data_to_json(cumulative)
        new_links = [dataset[0] for dataset in cumulative]
        return links + download_urls(new_links ,depth + 1)

# main test
if __name__ == "__main__":
    start = datetime.datetime.now()
    access = try_open_url(root)
    json.dump({"url_0": {"path": root ,"depth": 0 ,"access": access}} ,open(json_path ,"w") ,indent=4)
    if access:
        visited.append(root)
        links = download_urls([root])
        assert len(set(links)) == len(links)
    end = datetime.datetime.now()
    print("\nrun time: " + str(end - start))
