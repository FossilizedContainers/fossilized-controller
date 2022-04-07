import lipd
from flask import *
from lipd import *
from json import *
import os
import zipfile

'''
1. Refactor code so it's more aligned to Flask's convention and similar to this example:
        https://www.askpython.com/python-modules/flask/flask-rest-api

        Would solve Pycharm's request for handle_post to have a parameter

2. Look into the production deployment for Flask:
        https://flask.palletsprojects.com/en/1.1.x/deploying/
        https://flask.palletsprojects.com/en/1.1.x/tutorial/deploy/

'''

app = Flask(__name__)


class Adapter:

    def __init__(self, app):
        self.server = app

        self.reconstruction = None

        self.parameters = None
        self.inputs = None
        self.output_files = []

        # rename to initial_wd
        self.initial_working_dir = None

    def start_server(self):
        self.server.run(host='0.0.0.0', port=4000, debug=True)

    def stop_server(self):
        # self.server.stop()
        return

    def register(self, callback):
        self.reconstruction = callback
        return

    # function to get the list of files from the json file
    def get_files(self):
        # using the json key "inputs" to return the files
        return self.inputs

    # function to get the list of parameters from the json file
    def get_parameters(self):
        # using the json key "parameters" to return the parameters
        return self.parameters

    def get_output_files(self):
        return self.output_files

    # TODO: check if directory or file exists
    # TODO: location points to a directory
    def set_output_files(self, location):
        temp_path = os.path.abspath(location)
        self.reset_wd()

        if self.output_files:
            for i in self.output_files:
                if temp_path == i:
                    return

        self.output_files.append(temp_path)

    def reset_wd(self):
        os.chdir(self.initial_working_dir)

    # function to read the lipd files and store them in variables
    # Main Steps of Function:
    #   1. Parse metadata.JSON (finished)
    #   2. Save metadata.JSON["parameters"] in the adapter's parameters field. Save metadata.JSON["inputs"] in
    #               adapter's inputs field. (finished)
    #   3. Store all other files in adapter's inputs dictionary with file name as key and file data as value
    #               (in-progress)
    #   4. Run the reconstruction with "exec(adapter.reconstruction)" ()
    #   5. Compress the files at adapter.output_files and send back in HTTP Response message
    @app.route('/', methods=['POST'])
    def handle_post():
        # Issue: To use Python's None type, the JSON file must use null instead
        # Issue: To use Python's boolean values, the JSON file must use all lowercase for Booleans

        # Potential issue: Users must know JSON only allows double quotes
        # Potential issue: Users must know JSON keys must be strings
        metadata = json.loads(request.files['metadata'].read())

        global_adapter.parameters = metadata['parameters']
        global_adapter.inputs = metadata['inputs']

        # Reads in the input files, request.files is a dictionary of this object:
        #   https://werkzeug.palletsprojects.com/en/2.0.x/datastructures/#werkzeug.datastructures.FileStorage

        # For inputs, the  key, value pair is specific:
        #       key = the shorthand for file, should mirror the name in the POST request argument
        #       value = the location of the file; e.g.
        #                   "WMI_Lear.nc"
        #                   "nc-files/WMI_Lear.nc"
        #                   "data-files/nc-files/WMI_Lear.nc"
        #
        #       IMPORTANT: Unless you intend for the file to be stored in the relation to the root directory and not the
        #                  current working directory, DO NOT ADD A FORWARD OR BACK SLASH the the beginning of value /
        #                  file location. An example of this is:
        #                           "/WMI_Lear.nc"
        global_adapter.initial_working_dir = os.getcwd()

        for file in request.files:
            if file != "metadata":
                # to preserve the subdirectories from the metadata.JSON, uses the "name" argument from the POST request
                # and looks up the name in the metadata.JSON to see what file structure to preserve
                new_path = os.path.abspath(global_adapter.inputs[file])
                new_dirs = os.path.split(new_path)[0]

                if not os.path.isdir(new_dirs):
                    # 666 = read and write permissions for all
                    os.makedirs(new_dirs, 666, exist_ok=True)

                # save files based on the current working directory + metadata.JSON values
                request.files[file].save(new_path)

                # save location of files
                global_adapter.inputs[file] = new_path

                # if file.filename has .lpd extension, try to use readLipd and throw error if it fails
                if (os.path.splitext(request.files[file].filename))[1] == ".lpd":
                    if len(lipd.readLipd(new_path)) == 0:
                        return "File: " + file + " did not pass the readLipd", 500

            # saving a file changes the cwd and produces unintended behavior if not reset to its initial value
            global_adapter.reset_wd()

        # run the reconstruction
        global_adapter.reconstruction(global_adapter)

        # any reading done in the reconstruction will change the cwd and while there are no plans for multiple pings to
        # the adapter, if the server is pinged multiple times, the file structure produces unintended behavior
        global_adapter.reset_wd()

        # send output files in HTTP Response message
        zip_handler = zipfile.ZipFile('response_data.zip', 'w', zipfile.ZIP_DEFLATED)

        for location in global_adapter.output_files:
            if os.path.isfile(location):
                zip_handler.write(location, arcname=os.path.relpath(location))
            else:
                for root, dirs, files in os.walk(location, topdown=False):
                    for file in files:
                        temp_zip_location = \
                            os.path.relpath(os.path.join(root, file), start=global_adapter.initial_working_dir)
                        zip_handler.write(os.path.join(root, file), arcname=temp_zip_location)

        zip_handler.close()

        return send_from_directory(global_adapter.initial_working_dir, "response_data.zip")


# create global adapter instance
global_adapter = Adapter(app)