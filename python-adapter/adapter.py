import lipd
from flask import *
from lipd import *
from json import *

app = Flask(__name__)


class Adapter:

    def __init__(self, server):
        self.server = server

        self.climate_model = None

        self.parameters = None
        self.input_files = None
        self.output_files = None

    def start_server(self):
        self.server.run(host='0.0.0.0', port=4000)

    def stop_server(self):
        return

    def register(self, callback):
        self.climate_model = callback
        return callback

    # function to get the list of files from the json file
    def get_files(self):
        # using the json key "inputs" to return the files
        return self.input_files

    # function to get the list of parameters from the json file
    def get_parameters(self):
        # using the json key "parameters" to return the parameters
        return self.parameters

    def get_output_files(self):
        return self.output_files

    def set_output_files(self, str_array):
        self.output_files.append(str_array)


# create global adapter instance
adapter = Adapter(app)


# function to read the lipd files and store them in variables
@app.route('/', methods=['POST'])
def handle_post():
    metadata = json.loads(request.files['metadata.json'].read())
    # Potential issue: how JSON conversion handles None type!
    # Potential issue: Users must know JSON only allows double quotes
    # Potential issue: Users must know JSON keys must be strings


    adapter.parameters = metadata['parameters']
    adapter.input_files = metadata['input_files']

    # read the input lipd files
    adapter.input_files = {}
    for entry in adapter.input_files:
        file = request.files[entry]
        file.save(entry)

        # change below so not assume all input files are lipd
        # adapter.input_files[entry] = lipd.readLipd("./" + entry)

    adapter.climate_model()

    # the file(s) generated being returned from their directory - temporary test file for now
    return send_from_directory("./static/", "test.nc")
