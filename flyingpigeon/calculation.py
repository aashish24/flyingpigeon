
import logging
LOGGER = logging.getLogger("PYWPS")


from flyingpigeon.config import testdata_path

from flyingpigeon.config import testdata_path
from os import path
from os import listdir


def fieldmean(resource):
    """
    calculating of a weighted field mean

    :param resource: str or list of str containing the netCDF files pathes

    :return list: timeseries of the averaged values per timepstep
    """
    from flyingpigeon.utils import get_values, get_coordinates, get_index_lat
    from numpy import radians, average, cos, sqrt, array

    data = get_values(resource)  # np.squeeze(ds.variables[variable][:])
    dim = data.shape
    LOGGER.debug(data.shape)

    if len(data.shape) == 3:
        # TODO if data.shape == 2 , 4 ...
        lats, lons = get_coordinates(resource, unrotate=False)
        lats = array(lats)
        if len(lats.shape) == 2:
            lats = lats[:, 0]
        else:
            LOGGER.debug('Latitudes not reduced to 1D')
        # TODO: calculat weighed average with 2D lats (rotated pole coordinates)
        # lats, lons = get_coordinates(resource, unrotate=False)
        # if len(lats.shape) == 2:
        #     lats, lons = get_coordinates(resource)

        lat_index = get_index_lat(resource)
        LOGGER.debug('lats dimension %s ' % len(lats.shape))
        LOGGER.debug('lats index %s' % lat_index)

        lat_w = sqrt(cos(lats * radians(1)))
        meanLon = average(data, axis=lat_index, weights=lat_w)
        meanTimeserie = average(meanLon, axis=1)
        LOGGER.debug('fieldmean calculated')
    else:
        LOGGER.error('not 3D shaped data. Average can not be calculated')
    return meanTimeserie
