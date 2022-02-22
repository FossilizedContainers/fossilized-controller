import lipd
from flask import *
from lipd import *
from json import *

app = Flask(__name__)


class Adapter:

    def __init__(self, server):
        self.server = server
        self.parameters = None
        self.inputs = None
        self.input_lipds = None
        self.climate_model = None
        self.output_file = None

    def start(self):
        self.server.run(host='0.0.0.0', port=4000)

    def register(self, callback):
        self.climate_model = callback
        return callback


# create global adapter instance
adapter = Adapter(app)


# function to read the lipd files and store them in variables
@app.route('/', methods=['POST'])
def handle_post():
    metadata = json.loads(request.files['metadata.json'].read())
    adapter.parameters = metadata['parameters']
    adapter.inputs = metadata['inputs']

    # read the input lipd files
    adapter.input_lipds = {}
    for entry in adapter.inputs:
        file = request.files[entry]
        file.save(entry)
        adapter.input_lipds[entry] = lipd.readLipd("./" + entry)

    adapter.climate_model()

    # the file(s) generated being returned from their directory - temporary test file for now
    return send_from_directory("./static/", "test.nc")
