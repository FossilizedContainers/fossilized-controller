#%load_ext autoreload
#%autoreload 2

## These are ones you want to import for the adapter
# import os
import sys
import lipd


# import pythonAdapter, assumes in ../python-adapter/
# you can delete these lines if the adapter.py file is in the current directory
tests_dir = os.path.dirname(os.path.realpath(__file__))
fc_dir = os.path.dirname(tests_dir)
python_adapter_dir = os.path.join(fc_dir, "python-adapter")
sys.path.append(python_adapter_dir)


# import the adapter
import adapter

# these are the original imports
import LMRt
import os
import numpy as np
import pandas as pd
import xarray as xr


# the first step is to wrap your code around a basic function passing in the adapter
def lmrt_wrapper(adapter):
    # preprocessing
    print("\n======== Preprocessing ========\n")

    # ===Adapter work starts here===
    files = adapter.get_files()
    config = files['configs']
    parameters = adapter.get_parameters()
    print(parameters)

    # grabbing the specific parameter and saving it
    recon_param = parameters['recon_seeds']
    # ===Adapter work ends here===

    print(config)

    job = LMRt.ReconJob()
    # orginially this was a hardocded path, but now its using the path from
    # the get_files() function
    job.load_configs(cfg_path=config, verbose=True)
    job.load_proxydb(verbose=True)
    job.filter_proxydb(verbose=True)
    job.seasonalize_proxydb(verbose=True)
    job.load_prior(verbose=True)
    job.load_obs(verbose=True)
    #%%time
    job_dirpath = job.configs['job_dirpath']
    seasonalized_prior_path = os.path.join(job_dirpath, 'seasonalized_prior.pkl')
    seasonalized_obs_path = os.path.join(job_dirpath, 'seasonalized_obs.pkl')
    prior_loc_path = os.path.join(job_dirpath, 'prior_loc.pkl')
    obs_loc_path = os.path.join(job_dirpath, 'obs_loc.pkl')
    calibed_psm_path = os.path.join(job_dirpath, 'calibed_psm.pkl')

    job.calibrate_psm(
        seasonalized_prior_path=seasonalized_prior_path,
        seasonalized_obs_path=seasonalized_obs_path,
        prior_loc_path=prior_loc_path,
        obs_loc_path=obs_loc_path,
        calibed_psm_path=calibed_psm_path,
        verbose=True,
    )
    job.forward_psm(verbose=True)
    job.seasonalize_prior(verbose=True)
    job.regrid_prior(verbose=True)
    job.save()

    # The above equals to below:
    # del(job.seasonalized_prior)
    # del(job.seasonalized_obs)
    # pd.to_pickle(job, os.path.join(job_dirpath, 'job.pkl'))

    print("\n======== Data Assimilation ========\n")

    # Data assimilation
    # %%time
    # job_dirpath = '...'  # set a correct directory path
    # job = pd.read_pickle(os.path.join(job_dirpath, 'job.pkl'))

    # Here is our param from the get_parameters() function
    job.run(recon_seeds=np.arange(recon_param), verbose=True)

    # Adding every produced recon file
    # === Adapter work starts here ===
    # calibed_path = os.path.abspath('./recon/calibed_psm.pkl')
    # adapter.set_output_files(calibed_path)
    #
    # job_config_path = os.path.abspath('./recon/job_configs.yml')
    # adapter.set_output_files(job_config_path)
    #
    # _path = os.path.abspath('./recon/')
    # adapter.set_output_files(_path)
    #
    # _path = os.path.abspath('./recon/')
    # adapter.set_output_files(_path)
    #
    # _path = os.path.abspath('./recon/')
    # adapter.set_output_files(_path)
    #
    # _path = os.path.abspath('./recon/')
    # adapter.set_output_files(_path)
    #
    # _path = os.path.abspath('./recon/')
    # adapter.set_output_files(_path)
    #
    # _path = os.path.abspath('./recon/')
    # adapter.set_output_files(_path)
    #
    # _path = os.path.abspath('./recon/')
    # adapter.set_output_files(_path)
    # == Adapter work ends here ===

    print("\n======== Preview of results ========\n")
    # Preview of Results
    # create the res object for reconstruction results
    res = LMRt.ReconRes(job.configs['job_dirpath'], verbose=True)
    # get the varialbes from the recon_paths
    res.get_vars(['tas', 'nino3.4'], verbose=True)
    # plot the tas field
    fig, ax = res.vars['tas'].field_list[0].plot()
    fig.savefig("./figure1.png")

    # === Adapter work starts here ===
    figure1_path = os.path.abspath('./figure1.png')
    adapter.set_output_files(figure1_path)
    # == Adapter work ends here ===


    # plot and validate the NINO3.4
    from scipy.io import loadmat

    data = loadmat('./data/obs/NINO34_BC09.mat')
    syr, eyr = 1873, 2000
    nyr = eyr-syr+1
    nino34 = np.zeros(nyr)
    for i in range(nyr):
        nino34[i] = np.mean(data['nino34'][i*12:12+i*12])

    target_series = LMRt.Series(time=np.arange(syr, eyr+1), value=nino34, label='BC09')

    fig, ax = res.vars['nino3.4'].validate(target_series, verbose=True).plot(xlim=[1880, 2000])
    fig.savefig("./figure2.png")
    # === Adapter work starts here ===
    figure2_path = os.path.abspath('./figure2.png')
    adapter.set_output_files(figure2_path)
    # == Adapter work ends here ===

    return

# have to call adapter in the adapter.py file as adapter.adapter
adapter = adapter.global_adapter
# send in the name of your reconstruction wrapper function
adapter.register(lmrt_wrapper)
adapter.start_server()
