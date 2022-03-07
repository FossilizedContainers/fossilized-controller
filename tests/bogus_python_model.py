import os
import sys
import lipd

# import pythonAdapter, assumes in ../python-adapter/
tests_dir = os.path.dirname(os.path.realpath(__file__))
fc_dir = os.path.dirname(tests_dir)
python_adapter_dir = os.path.join(fc_dir, "python-adapter")
sys.path.append(python_adapter_dir)

import adapter


def fake_model(adapter):
    # check to see inside function
    print("\n---\nStart of the fake_model function\n---\n")

    # the parameters are handed to you by the adapter
    files = adapter.get_files()

    # use the parameters given by the adapter to get the binary data of the LiPD file
    lipd.readLipd(files['weldeab'])

    # get the binary data of the NetCDF file
    net_cdf_path = files['net_cdf']

    # mark the NetCDF file as an output file
    adapter.set_output_files(net_cdf_path)

    return

# have to call adapter in the adapter.py file as adapter.adapter
adapter = adapter.global_adapter

adapter.register(fake_model)
adapter.start_server()
