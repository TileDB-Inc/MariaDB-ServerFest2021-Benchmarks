# MariaDB-ServerFest2021-Benchmarks

## Preqs

This assumes you are going to be using a Ubuntu 20.04 image on a AWS EC2
m5.4xlarge host. There should be a 512GB EBS GP3 volume mounted to `/data`

## Packages

```
sudo apt-get install -y \
  gosu \
  pwgen \
  tzdata \
  gcc \
  g++ \
  build-essential \
  libasan5 \
  bison \
  chrpath \
  cmake \
  gdb \
  gnutls-dev \
  libaio-dev \
  libboost-dev \
  libboost-filesystem-dev \
  libboost-thread-dev \
  libboost-regex-dev \
  libboost-date-time-dev \
  libboost-chrono-dev \
  libboost-atomic-dev \
  libdbd-mysql \
  libjudy-dev \
  libncurses5-dev \
  libpam0g-dev \
  libpcre3-dev \
  libreadline-gplv2-dev \
  libstemmer-dev \
  libssl-dev \
  libnuma-dev \
  libxml2-dev \
  lsb-release \
  perl \
  psmisc \
  zlib1g-dev \
  libcrack2-dev \
  cracklib-runtime \
  libjemalloc-dev \
  libsnappy-dev \
  liblzma-dev \
  libzmq3-dev \
  uuid-dev \
  ccache \
  git \
  wget \
  libcurl4-openssl-dev \
  libcurl4 \
  flex \
  pkg-config \
  libzstd-dev \
  liblz4-dev \
  libbz2-dev \
  python3-pip \
  python3-dev
  ```

## Clone Repos
```
git clone https://github.com/mariadb/server -b mariadb-10.5.12
git clone https://github.com/TileDB-Inc/TileDB-MariaDB -b 0.10.1
```

Symlink MyTile storage engine
```
ln -s ~/TileDB-MariaDB ~/server/storage/mytile
```

## Install Prebuilt TileDB

Note, MyTile can also build TileDB from source. We'll use prebuilt package for simplicity and reproducibility of benchmark.

```
wget https://github.com/TileDB-Inc/TileDB/releases/download/2.4.0/tiledb-linux-x86_64-2.4.0-baf64e1.tar.gz
```

Valid SHA256 matches for download:
```
sha256sum tiledb-linux-x86_64-2.4.0-baf64e1.tar.gz  | grep 0a956f9808585b849bc19fdeef9a4a15021d820ba8a74567c6361309836a33df
```

Extract to /usr/local
```
sudo tar -C /usr/local/ -xf tiledb-linux-x86_64-2.4.0-baf64e1.tar.gz
sudo ldconfig
```

## Build MariaDB

Next its time to build and install MariaDB. We will build only a few storage enignes used for the benchmarking.
```
mkdir build
cd build
cmake -DPLUGIN_MYTILE=YES -DPLUGIN_INNODB=YES -DPLUGIN_TOKUDB=NO -DPLUGIN_ROCKSDB=YES -DPLUGIN_MROONGA=NO -DPLUGIN_SPIDER=NO -DPLUGIN_SPHINX=NO -DPLUGIN_FEDERATED=NO -DPLUGIN_FEDERATEDX=NO -DPLUGIN_CONNECT=NO -DCMAKE_BUILD_TYPE=Release -SWITH_DEBUG=0 -DBUILD_CONFIG=mysql_release -DWITH_EMBEDDED_SERVER=OFF -DCMAKE_INSTALL_PREFIX=/opt/mariadb_server_10.5.12 ..
make -j$(nproc)
make install
  ```

## Setup MariaDB


First copy configuration

```
sudo cp my.cnf /etc/my.cnf
```

Next install MariaDB database

```
/opt/mariadb_server_10.5.12/scripts/mariadb-install-db --defaults-file /etc/mysql/my.cnf --datadir=/data
```

## Loading Data

### TileDB

First we'll create the TileDB Array, we'll then use this array to insert into the other tables.

Install TileDB-Py and dependencies of ingestion script
```
pip install --user tiledb progressbar pandas
```

Next lets run the ingestion script, this creates and array in `/data/test/nyc_yellow_taxi_tiledb`

```
python nyc_taxi_ingestion.py
```

```
CREATE TABLE `nyc_yellow_taxi_tiledb` ENGINE=TileDB uri='/data/test/nyc_yellow_taxi_tiledb';
```

### InnoDB


```
CREATE TABLE `nyc_yellow_taxi_innodb_zlib`
(`tpep_pickup_datetime` timestamp(6) NOT NULL,
   `PULocationID` bigint(20) NOT NULL,
   `congestion_surcharge` double NOT NULL DEFAULT 0,
   `improvement_surcharge` double NOT NULL DEFAULT 0,
   `VendorID` double NOT NULL DEFAULT 0,
    `payment_type` double NOT NULL DEFAULT 0,
    `tpep_dropoff_datetime` timestamp(6),
    `DOLocationID` bigint(20) NOT NULL ,
    `mta_tax` double NOT NULL DEFAULT 0,
    `passenger_count` double NOT NULL DEFAULT 0,
    `trip_distance` double NOT NULL DEFAULT 0,
    `RatecodeID` double NOT NULL DEFAULT 0,
    `store_and_fwd_flag` text NOT NULL,
    `total_amount` double NOT NULL DEFAULT 0,
    `fare_amount` double NOT NULL DEFAULT 0,
    `extra` double NOT NULL DEFAULT 0,
    `tip_amount` double NOT NULL DEFAULT 0,
    `tolls_amount` double NOT NULL DEFAULT 0,
    PRIMARY KEY (`tpep_pickup_datetime`,`PULocationID`)
) ENGINE=InnoDB;

INSERT IGNORE INTO nyc_yellow_taxi_innodb_zlib select tpep_pickup_datetime, PULocationID, congestion_surcharge, improvement_surcharge, VendorID,payment_type,tpep_dropoff_datetime,DOLocationID,mta_tax,passenger_count,trip_distance,RatecodeID,store_and_fwd_flag,total_amount,fare_amount,extra,tip_amount,tolls_amount FROM nyc_yellow_taxi_tiledb;
```

### RocksDB

```
CREATE TABLE `nyc_yellow_taxi_myrocks`
(`tpep_pickup_datetime` timestamp(6) NOT NULL,
   `PULocationID` bigint(20) NOT NULL,
   `congestion_surcharge` double NOT NULL DEFAULT 0,
   `improvement_surcharge` double NOT NULL DEFAULT 0,
   `VendorID` double NOT NULL DEFAULT 0,
   `payment_type` double NOT NULL DEFAULT 0,
   `tpep_dropoff_datetime` timestamp(6),
   `DOLocationID` bigint(20) NOT NULL ,
   `mta_tax` double NOT NULL DEFAULT 0,
   `passenger_count` double NOT NULL DEFAULT 0,
   `trip_distance` double NOT NULL DEFAULT 0,
   `RatecodeID` double NOT NULL DEFAULT 0,
   `store_and_fwd_flag` text NOT NULL,
   `total_amount` double NOT NULL DEFAULT 0,
   `fare_amount` double NOT NULL DEFAULT 0,
   `extra` double NOT NULL DEFAULT 0,
   `tip_amount` double NOT NULL DEFAULT 0,
   `tolls_amount` double NOT NULL DEFAULT 0,
   PRIMARY KEY (`tpep_pickup_datetime`,`PULocationID`)
) ENGINE=ROCKSDB;

SET session sql_log_bin=0;
SET session rocksdb_bulk_load_allow_unsorted=1;
SET session rocksdb_bulk_load=1;
INSERT IGNORE INTO nyc_yellow_taxi_myrocks select tpep_pickup_datetime, PULocationID, congestion_surcharge, improvement_surcharge, VendorID,payment_type,tpep_dropoff_datetime,DOLocationID,mta_tax,passenger_count,trip_distance,RatecodeID,store_and_fwd_flag,total_amount,fare_amount,extra,tip_amount,tolls_amount FROM nyc_yellow_taxi_innodb_zlib;
SET session rocksdb_bulk_load=0;
```

## Benchmarks

See [Benchamrks.md](Benchmarks.md)