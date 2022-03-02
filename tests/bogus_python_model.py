import os
import sys
import lipd

# import pythonAdapter, assumes in ../python-adapter/
tests_dir = os.path.dirname(__file__)
python_adapter_dir = os.path.join(tests_dir, '..', 'python-adapter')
sys.path.append(python_adapter_dir)

import adapter

def fakeModel(adapter):

    # the parameters are handed to you by the adapter
    params = adapter.get_parameters()

    # use the parameters given by the adapter to get the binary data of the LiPD file
    lipd_object = lipd.readLipd(params['lipd_file'])

    # check if LiPD file could be parsed correctly
    if len(lipd_object) == 0:
        return "Invalid LiPD file"

    # get the binary data of the NetCDF file
    net_cdf_path = params['net_cdf_file']

    # mark the NetCDF file as an output file
    adapter.set_output_files(net_cdf_path)

    return

# adapter = new Python Adapter

# adapter.register_model("fakeModel(adapter)")
# adapter.start_server()