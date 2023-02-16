
class ILinks:

    # create library of sources and result file
    def create_library_sources(self):
        pass

    # create custom file format by user choice
    def create_file_format(self):
        pass

    # create dataset information for link
    def create_dataset(self, link, depth):
        pass

    # check access to url
    def try_open_url(self, link):
        pass

    # read latest data from file results
    def read_from_file(self):
        pass

    # write new data to file results
    def write_to_file(self, data):
        pass

    # extract urls set from general url
    def extract_urls(self, link):
        pass

    # try open url and response html content
    def try_get_html(self, link):
        pass

    # fix incomplete urls to access active
    def fix_urls(self, links):
        pass

    # download all data from main url up to max depth
    def download_urls(self, links, depth=0):
        pass

    # invoke order of actions for progress
    def run_progress(self):
        pass
