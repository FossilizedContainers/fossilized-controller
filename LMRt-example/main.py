import LMRt
import os
import numpy as np
import pandas as pd
import xarray as xr


# preprocessing
job = LMRt.ReconJob()
job.load_configs(cfg_path='/PAGES2k_CCSM4_GISTEMP/configs.yml', verbose=True)
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

# The above equals to below:
# del(job.seasonalized_prior)
# del(job.seasonalized_obs)
# pd.to_pickle(job, os.path.join(job_dirpath, 'job.pkl'))


# Data assimilation
# %%time
# job_dirpath = '...'  # set a correct directory path
# job = pd.read_pickle(os.path.join(job_dirpath, 'job.pkl'))
job.run(recon_seeds=np.arange(1), verbose=True)


# Preview of Results
# create the res object for reconstruction results
res = LMRt.ReconRes(job.configs['job_dirpath'], verbose=True)
# get the varialbes from the recon_paths
res.get_vars(['tas', 'nino3.4'], verbose=True)
# plot the tas field
fig, ax = res.vars['tas'].field_list[0].plot()
fig.savefig("/figure1.png")


# plot and validate the NINO3.4
from scipy.io import loadmat

data = loadmat('./PAGES2k_CCSM4_GISTEMP/data/obs/NINO34_BC09.mat')
syr, eyr = 1873, 2000
nyr = eyr-syr+1
nino34 = np.zeros(nyr)
for i in range(nyr):
    nino34[i] = np.mean(data['nino34'][i*12:12+i*12])

target_series = LMRt.Series(time=np.arange(syr, eyr+1), value=nino34, label='BC09')

fig, ax = res.vars['nino3.4'].validate(target_series, verbose=True).plot(xlim=[1880, 2000])
fig.savefig("/figure2.png")
