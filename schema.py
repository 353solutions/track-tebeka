import pandera as pa
import pandas as pd

track_schema = pa.DataFrameSchema({
    'time': pa.Column(pd.DatetimeTZDtype('ns', 'UTC')),
    'lat': pa.Column(float, checks=pa.Check.in_range(-90, 90)),
    'lng': pa.Column(float, checks=pa.Check.in_range(-180, 180)),
    'height': pa.Column(float, checks=pa.Check.in_range(-422, 8849)),
})