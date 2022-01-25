import numpy as np
import pandas as pd
from pandera import check_input
from pandera import check_output
import logging

# relative import
from .schema import track_schema

lat_km = 92
lng_km = 111


@check_output(track_schema)
def load_track(file_name):
    logging.info('loading %s', file_name)
    # The below will create a new string even if INFO level not enabled
    # logging.info(f'loading {file_name}')
    df = pd.read_csv(file_name, parse_dates=['time'])
    logging.info('%s loaded %d rows', file_name, len(df))
    return df


# type hints
def distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Return Euclidean distance (in kilometers) between two coordinates)

    >>> distance(0, 0, 1, 1)
    144.1700384962146
    """
    delta_lat = (lat1 - lat2) * lat_km
    delta_lng = (lng1 - lng2) * lng_km
    return np.hypot(delta_lat, delta_lng)


@check_input(track_schema)
def running_speed(df):
    dist_km = distance(
        df['lat'], df['lng'],
        df['lat'].shift(), df['lng'].shift(),
    )

    time_hours = df['time'].diff() / pd.Timedelta(hours=1)
    return dist_km / time_hours


def plot_speed(date, speed_kmh):
    ax = speed_kmh.plot.box(title=f'{date} Run')
    ax.set_xticks([])  # Remove "None"
    ax.set_ylabel(r'Running speed $\frac{km}{h}$')
    return ax
