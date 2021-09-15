# MariaDB-ServerFest2021-Benchmarks

# Packages

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
  libbz2-dev
  ```

## Clone Repos
```
git clone https://github.com/mariadb/server -b mariadb-10.5.12
git clone https://github.com/TileDB-Inc/TileDB-MariaDB -b 0.10.0
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
