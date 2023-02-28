from abc import ABC, abstractmethod

class ILinks(ABC):

    # create library of sources and result file
    @abstractmethod
    def create_library_sources(self):
        pass

    # create custom file format by user choice
    @abstractmethod
    def create_file_format(self):
        pass

    # create dataset information for link
    @abstractmethod
    def create_dataset(self, link, depth):
        pass

    # check access to url
    @abstractmethod
    def try_open_url(self, link):
        pass

    # extract urls set from general url
    @abstractmethod
    def extract_urls(self, link):
        pass

    # try open url and response html content
    @abstractmethod
    def try_get_html(self, link):
        pass

    # fix incomplete urls to access active
    @abstractmethod
    def fix_urls(self, links):
        pass

    # download all data from main url up to max depth
    @abstractmethod
    def download_urls(self, links, depth=0):
        pass

    # invoke order of actions for progress
    @abstractmethod
    def run_progress(self):
        pass
