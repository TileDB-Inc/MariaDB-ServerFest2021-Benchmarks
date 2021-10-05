import tiledb
import concurrent.futures
import progressbar
import numpy
from pathlib import Path
import pandas

array_uri = "/data/test/nyc_yellow_taxi_tiledb"
header_2016_2020 = [
    "VendorID",
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
    "passenger_count",
    "trip_distance",
    "RatecodeID",
    "store_and_fwd_flag",
    "PULocationID",
    "DOLocationID",
    "payment_type",
    "fare_amount",
    "extra",
    "mta_tax",
    "tip_amount",
    "tolls_amount",
    "improvement_surcharge",
    "total_amount",
]

header_2015 = [
    # pickup_longitude,pickup_latitude
    "VendorID",
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
    "passenger_count",
    "trip_distance",
    "pickup_longitude",
    "pickup_latitude",
    "RatecodeID",
    "store_and_fwd_flag",
    "dropoff_longitude",
    "dropoff_latitude",
    "payment_type",
    "fare_amount",
    "extra",
    "mta_tax",
    "tip_amount",
    "tolls_amount",
    "improvement_surcharge",
    "total_amount",
]
dtypes = {
    "VendorID": "float64",
    # "tpep_pickup_datetime": "datetime64[ns]",
    # "tpep_dropoff_datetime": "datetime64[ns]",
    "passenger_count": "float64",
    "trip_distance": "float64",
    "RatecodeID": "float64",
    "store_and_fwd_flag": "str",
    # "PULocationID": "int64",
    # "DOLocationID": "int64",
    "payment_type": "float64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
}


converters = {
    "PULocationID": lambda x: int(x) if x else None,
    "DOLocationID": lambda x: int(x) if x else None,
}


def ingest_2015(array_uri, csv_file, taxi_zone_shapes):
    vfs = tiledb.VFS()
    csv_file = tiledb.FileIO(vfs, csv_file, mode="rb")
    df = pandas.read_csv(
        csv_file,
        index_col=["tpep_pickup_datetime", "PULocationID"],
        parse_dates=["tpep_dropoff_datetime", "tpep_pickup_datetime"],
        skiprows=1,
        names=header_2016_2020,
        usecols=[i for i in range(len(header_2016_2020))],
        dtype=dtypes,
        # dtype={"store_and_fwd_flag": "bool"},
        # usecols = [i for i in range(n)]
    )
    df["congestion_surcharge"] = numpy.float64(None)

    tiledb.from_pandas(array_uri, df, mode="append", fillna={"store_and_fwd_flag": ""})


def ingest_2016(array_uri, csv_file):
    vfs = tiledb.VFS()
    csv_file = tiledb.FileIO(vfs, csv_file, mode="rb")
    df = pandas.read_csv(
        csv_file,
        index_col=["tpep_pickup_datetime", "PULocationID"],
        parse_dates=["tpep_dropoff_datetime", "tpep_pickup_datetime"],
        skiprows=1,
        names=header_2016_2020,
        usecols=[i for i in range(len(header_2016_2020))],
        dtype=dtypes,
        # dtype={"store_and_fwd_flag": "bool"},
    )
    df["congestion_surcharge"] = numpy.float64(None)
    tiledb.from_pandas(array_uri, df, mode="append", fillna={"store_and_fwd_flag": ""})


def create_array(array_uri):

    schema = tiledb.ArraySchema(
        domain=tiledb.Domain(
            [
                tiledb.Dim(
                    name="tpep_pickup_datetime",
                    domain=(
                        numpy.datetime64("1677-09-21T00:12:43.145224193"),
                        numpy.datetime64("2262-04-11T23:47:16.854774807"),
                    ),
                    tile=None,
                    dtype="datetime64[ns]",
                    filters=tiledb.FilterList(
                        [
                            tiledb.ZstdFilter(level=-1),
                        ]
                    ),
                ),
                tiledb.Dim(
                    name="PULocationID",
                    domain=(-9223372036854775808, 9223372036854774807),
                    tile=None,
                    dtype="int64",
                    filters=tiledb.FilterList(
                        [
                            tiledb.ZstdFilter(level=-1),
                        ]
                    ),
                ),
            ]
        ),
        attrs=[
            tiledb.Attr(
                name="VendorID",
                dtype="float64",
                var=False,
                nullable=False,
                filters=tiledb.FilterList(
                    [
                        tiledb.ZstdFilter(level=-1),
                    ]
                ),
            ),
            tiledb.Attr(
                name="tpep_dropoff_datetime",
                dtype="datetime64[ns]",
                var=False,
                nullable=False,
                filters=tiledb.FilterList(
                    [
                        tiledb.ZstdFilter(level=-1),
                    ]
                ),
            ),
            tiledb.Attr(
                name="passenger_count",
                dtype="float64",
                var=False,
                nullable=False,
                filters=tiledb.FilterList(
                    [
                        tiledb.ZstdFilter(level=-1),
                    ]
                ),
            ),
            tiledb.Attr(
                name="trip_distance",
                dtype="float64",
                var=False,
                nullable=False,
                filters=tiledb.FilterList(
                    [
                        tiledb.ZstdFilter(level=-1),
                    ]
                ),
            ),
            tiledb.Attr(
                name="RatecodeID",
                dtype="float64",
                var=False,
                nullable=False,
                filters=tiledb.FilterList(
                    [
                        tiledb.ZstdFilter(level=-1),
                    ]
                ),
            ),
            tiledb.Attr(
                name="store_and_fwd_flag",
                dtype="ascii",
                var=True,
                nullable=False,
                filters=tiledb.FilterList(
                    [
                        tiledb.ZstdFilter(level=-1),
                    ]
                ),
            ),
            tiledb.Attr(
                name="DOLocationID",
                dtype="int64",
                var=False,
                nullable=False,
                filters=tiledb.FilterList(
                    [
                        tiledb.ZstdFilter(level=-1),
                    ]
                ),
            ),
            tiledb.Attr(
                name="payment_type",
                dtype="float64",
                var=False,
                nullable=False,
                filters=tiledb.FilterList(
                    [
                        tiledb.ZstdFilter(level=-1),
                    ]
                ),
            ),
            tiledb.Attr(
                name="fare_amount",
                dtype="float64",
                var=False,
                nullable=False,
                filters=tiledb.FilterList(
                    [
                        tiledb.ZstdFilter(level=-1),
                    ]
                ),
            ),
            tiledb.Attr(
                name="extra",
                dtype="float64",
                var=False,
                nullable=False,
                filters=tiledb.FilterList(
                    [
                        tiledb.ZstdFilter(level=-1),
                    ]
                ),
            ),
            tiledb.Attr(
                name="mta_tax",
                dtype="float64",
                var=False,
                nullable=False,
                filters=tiledb.FilterList(
                    [
                        tiledb.ZstdFilter(level=-1),
                    ]
                ),
            ),
            tiledb.Attr(
                name="tip_amount",
                dtype="float64",
                var=False,
                nullable=False,
                filters=tiledb.FilterList(
                    [
                        tiledb.ZstdFilter(level=-1),
                    ]
                ),
            ),
            tiledb.Attr(
                name="tolls_amount",
                dtype="float64",
                var=False,
                nullable=False,
                filters=tiledb.FilterList(
                    [
                        tiledb.ZstdFilter(level=-1),
                    ]
                ),
            ),
            tiledb.Attr(
                name="improvement_surcharge",
                dtype="float64",
                var=False,
                nullable=False,
                filters=tiledb.FilterList(
                    [
                        tiledb.ZstdFilter(level=-1),
                    ]
                ),
            ),
            tiledb.Attr(
                name="total_amount",
                dtype="float64",
                var=False,
                nullable=False,
                filters=tiledb.FilterList(
                    [
                        tiledb.ZstdFilter(level=-1),
                    ]
                ),
            ),
            tiledb.Attr(
                name="congestion_surcharge",
                dtype="float64",
                var=False,
                nullable=False,
                filters=tiledb.FilterList(
                    [
                        tiledb.ZstdFilter(level=-1),
                    ]
                ),
            ),
        ],
        cell_order="hilbert",
        # tile_order="hilbert",
        capacity=100000,
        sparse=True,
        allows_duplicates=True,
        coords_filters=tiledb.FilterList([tiledb.ZstdFilter(level=-1)]),
    )

    if not (tiledb.VFS().is_dir(array_uri)):
        tiledb.Array.create(array_uri, schema)


def list_data():
    files = tiledb.VFS().ls("s3://nyc-tlc/trip data/")

    files_with_schema_version = {}
    for f in files:
        if not f.startswith("s3://nyc-tlc/trip data/yellow_tripdata_"):
            continue
        filename = Path(f).stem
        year_month = filename.split("_")[2]
        year = int(year_month.split("-")[0])
        month = int(year_month.split("-")[1])

        if (year) >= 2019:
            files_with_schema_version[f] = "2019"
        elif (year == 2016 and month >= 7) or year == 2017 or year == 2018:
            files_with_schema_version[f] = "2016"
        elif year == 2015 or (year == 2016 and month < 7):
            files_with_schema_version[f] = "2015"
        elif year < 2015:
            files_with_schema_version[f] = "2009"
    return files_with_schema_version


def load_data(array_uri, files_with_schema_version):

    futures = []
    # max_workers=len(yellow_tripdata_2019_schema)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for csv_file in files_with_schema_version.items():
            if csv_file[1] == "2019":
                print(f"ingestion 2019 schema file {csv_file[0]} directly")
                futures.append(
                    executor.submit(
                        tiledb.from_csv,
                        array_uri,
                        csv_file[0],
                        mode="append",
                        index_col=["tpep_pickup_datetime", "PULocationID"],
                        parse_dates=["tpep_dropoff_datetime", "tpep_pickup_datetime"],
                        fillna={"store_and_fwd_flag": ""},
                        # dtype={"store_and_fwd_flag": "bool"},
                    )
                )
            elif csv_file[1] == "2016":
                print(
                    f"ingestion 2016 schema file {csv_file[0]} by adding null congestion"
                )
                futures.append(executor.submit(ingest_2016, array_uri, csv_file[0]))
            elif csv_file[1] == "2015":
                print(f"Skipping 2015 formatted file {csv_file[0]} for now")
            elif csv_file[1] == "2009":
                print(f"Skipping 2009 formatted file {csv_file[0]} for now")
            else:
                raise RuntimeError(f"Unknown csv schema version {csv_file[1]}")

        for future in progressbar.progressbar(futures):
            result = future.result()


def main():
    create_array(array_uri)
    files_with_schema_version = list_data()
    load_data(array_uri, files_with_schema_version)


if __name__ == "__main__":
    main()
