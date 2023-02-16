from formats.ILinks import ILinks
import progressbar # pip install progressbar2
from shared import consts
from shared.consts import visited, ignore, widgets
import datetime

class CSVFormat(ILinks):

    # static class variables
    file_path = ""
    datasets = []

    # constructor
    def __init__(self, root, max_depth):
        self.serial = consts.serial
        self.root = root
        self.max_depth = max_depth

    # give name for output file
    def get_name_to_file(self):
        timestamp = datetime.datetime.now().strftime('%m-%d-%Y %H-%M-%S')
        name_source = self.root.split('.')[1]
        if name_source == 'wikipedia':
            name_source = self.root.split('/')[-1].lower()
        CSVFormat.file_path = name_source + "_md" + str(self.max_depth) + "_" + timestamp + ".csv"
