import lipd

localLipd = \
    "C:/Users/mumbi/Documents/spring 2022/cs 486/fossilized-controller/test/lipd-files/GeoB9310_4.Weldeab.2014.lpd"

def fakeModel(bogus, lipd_file):

    lipd_object = lipd.readLipd(lipd_file)

    if len(lipd_object) == 0:
        return "Invalid LiPD file"

    net_cdf_path = "C:/Users/mumbi/Documents/spring 2022/cs 486/fossilized-controller/test/nc-files/WMI_Lear.nc"

    return net_cdf_path