from formats.ILinks import ILinks
import re
import requests
import progressbar
from tools import Settings
from tools.Settings import visited, ignore, widgets
import datetime
import json
import io
import os

class JsonFormat(ILinks):

    # constructor
    def __init__(self, root, max_depth):
        self.serial = Settings.serial
        self.root = root
        self.max_depth = max_depth

    # create library of sources and result file
    def create_library_sources(self):
        if not os.path.exists("sources"):
            os.mkdir("sources")
        timestamp = datetime.datetime.now().strftime('%m-%d-%Y %H-%M-%S')
        name_source = self.root.split('.')[1]
        if name_source == 'wikipedia':
            name_source = self.root.split('/')[-1].lower()
        if not os.path.exists("sources/" + name_source):
            os.mkdir("sources/" + name_source)
        self.file_path = "sources/" + name_source + "/" + name_source + "_md" + str(self.max_depth) + "_" + timestamp + ".json"

    # create json file
    def create_file_format(self):
        with io.open(self.file_path, "w", encoding='utf8') as file:
            json.dump({}, file, indent=4)

    # insert url data to file results if exist
    def add_data_to_json(self, link, depth):
        dataset = self.create_dataset(link, depth)
        if dataset:
            data = self.read_from_file()
            link, depth, access = dataset[1], dataset[2], dataset[3]
            key = 'url_' + str(self.serial)
            value = {
                "link": link,
                "depth": depth,
                "access": access,
            }
            data[key] = value
            self.serial += 1
            self.write_to_file(data)

    # create dataset information for link
    def create_dataset(self, link, depth):
        dataset = []
        if not link in visited:
            dataset = (self.serial, link, depth, self.try_open_url(link))
            visited.append(link)
        return dataset

    # check access to url
    def try_open_url(self, link):
        try:
            access = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'}, allow_redirects=False)
            return access.status_code in [200, 301, 302, 303, 403, 406, 500, 999]
        except:
            return False

    # read latest data from file results
    def read_from_file(self):
        with open(self.file_path, "r") as file:
            data = json.load(file)
        return data

    # write new data to file results
    def write_to_file(self, data):
        with io.open(self.file_path, "w", encoding='utf8') as file:
            json.dump(data, file, indent=4)

    # extract urls set from general url
    def extract_urls(self, link):
        try:
            response = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'}, allow_redirects=False)
            html = response.content.decode('latin1')
            extracts = re.findall('href="[https:]*[/{1,2}#]*[\w+.\-/=?_#]*"', html)
            fix_links = self.fix_urls([link.replace('href=', '').replace('"', '') for link in extracts])
            return fix_links
        except:
            return []

    # try open url and response html content
    def try_get_html(self, link):
        try:
            response = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'}, allow_redirects=False)
            html = response.content.decode('latin1')
            return html
        except:
            return ''

    # fix incomplete urls to access active
    def fix_urls(self, links):
        fix_links = []
        for link in links:
            if '?' in link:
                link = link[:link.find('?')]
            if '#' in link:
                link = link[:link.find('#')]
            if link.startswith('//'):
                link = 'https:' + link
            elif link.startswith('/') and len(link) > 1:
                link = 'https://' + self.root.split('/')[2] + link
            elif not '/' in link:
                link = 'https://' + self.root.split('/')[2] + '/' + link
            link = link[:-1] if link.endswith('/') else link
            if link and not link in visited:
                fix_links.append(link)
        return fix_links

    # download all data from main url up to max depth
    def download_urls(self, links, depth=0):
        if depth > self.max_depth:
            return []
        else:
            print("\nextract urls from " + str(self.root) + " in depth " + str(depth) + ":")
            bar = progressbar.ProgressBar(max_value=len(links), widgets=widgets).start()
            next = 0
            cumulative = []
            for link in links:
                if not link.split('.')[-1] in ignore:
                    self.add_data_to_json(link, depth)
                    extracts = list(set(self.extract_urls(link)))
                    cumulative = cumulative + extracts
                bar.update(next)
                next += 1
            return links + self.download_urls(cumulative, depth + 1)

    # invoke order of actions for progress
    def run_progress(self):
        self.create_library_sources()
        self.create_file_format()
        links = self.download_urls([self.root])
        assert len(set(links)) == len(links)
