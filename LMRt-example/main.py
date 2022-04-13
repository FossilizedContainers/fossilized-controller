import LMRt
import os
import numpy as np
import pandas as pd
import xarray as xr


# preprocessing
print("\n======== Preprocessing ========\n")

config = '/PAGES2k_CCSM4_GISTEMP/configs.yml'
recon_iterations = 1
figure = 'graph'

job = LMRt.ReconJob()
job.load_configs(config, verbose=True)
job.load_proxydb(verbose=True)
job.filter_proxydb(verbose=True)
job.seasonalize_proxydb(verbose=True)
job.load_prior(verbose=True)
job.load_obs(verbose=True)

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

print("\n======== Data Assimilation ========\n")
# Data assimilation
job.run(recon_seeds=np.arange(recon_iterations), verbose=True)


print("\n======== Preview of results ========\n")
# Preview of Results
# create the res object for reconstruction results
res = LMRt.ReconRes(job.configs['job_dirpath'], verbose=True)
# get the varialbes from the recon_paths
res.get_vars(['tas', 'nino3.4'], verbose=True)

if(figure_type == 'map'):

    # plot the tas field
    fig, ax = res.vars['tas'].field_list[0].plot()
    fig.savefig("./map.png")
elif(figure_type == 'graph'):
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
    fig.savefig("./graph.png")
else:
    print("not a valid figure parameter \n")
