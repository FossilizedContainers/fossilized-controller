import lipd
from flask import *
from lipd import *
from json import *

class pythonAdaptor:

    app = Flask(__name__)

    # will add more as we build
    def __init__(self):
        pass

    # function to read the lipd files and store them in variables
    @app.route('/', methods=['POST'])
    def server(self):
        metadata = json.loads(request.files['metadata.json'].read())
        parameters = self.get_parameters(metadata)
        inputs = self.get_files(metadata)

        # read the input lipd files
        input_lipds = {}
        for entry in inputs:
            file = request.files[entry]
            file.save(entry)
            input_lipds[entry] = lipd.readLipd("./" + entry)

        # here we would pass parameters & input_lipds to the climate model
        print(parameters)
        print(input_lipds)

        # fake NetCDF file that would really come from the climate model
        return send_from_directory("./static/", "test.nc")

    # function to add the parameters to a list and return that list
    def get_parameters(self, metadata):
        # using the json key to return the parameters
        return metadata['parameters']

    # function to add the files being used to a list and return the list
    def get_files(self, metadata):
        # using the json key to return the files
        return metadata['inputs']

    # setting the host and port for the server to run on
    app.run(host='0.0.0.0', port=4000)
