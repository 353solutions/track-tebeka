import numpy as np
import pandas as pd

lat_km = 92
lng_km = 111


def load_track(file_name):
    return pd.read_csv(file_name, parse_dates=['time'])


def distance(lat1, lng1, lat2, lng2):
    """Return Euclidean distance (in kilometers) between two coordinates)

    >>> distance(0, 0, 1, 1)
    144.1700384962146
    """
    delta_lat = (lat1 - lat2) * lat_km
    delta_lng = (lng1 - lng2) * lng_km
    return np.hypot(delta_lat, delta_lng)


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

# __name__ -> dunder name
if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    parser = ArgumentParser(description='Generate box plot of running speed')
    parser.add_argument('csv_file', help='CSV file', type=FileType('r'))
    parser.add_argument('out_file', help='Output file', type=FileType('w'))
    args = parser.parse_args()

    df = load_track(args.csv_file.name)
    speed = running_speed(df)
    ax = plot_speed('2022-01-23', speed)
    ax.figure.savefig(args.out_file.name)