# Benchmarks

The following sql statements are benchmarks.


## Full Table Scan

This query shows the pushdown of filters when a full scan is used because
the `WHERE` does not include any primary key fields.

### TileDB
```
select count(DOLocationID) from `nyc_yellow_taxi_tiledb` where DOLocationID = 127;
```

### InnoDB
```
select count(DOLocationID) from `nyc_yellow_taxi_innodb_zlib` where DOLocationID = 127;
```

### MyRocks
```
select count(DOLocationID) from `nyc_yellow_taxi_myrocks` where DOLocationID = 127;
```


## Primary Key Scan With Additional Predicate

This query shows the pushdown of filters when the primary key is used for the
index scan but there is additional condition on a non-indexed field.

### TileDB
```
select count(DOLocationID) from `nyc_yellow_taxi_tiledb` where tpep_pickup_datetime between '2016-07-31 20:31:45.000000' AND '2018-01-01 00:00:00.000000' AND PULocationID > 1 AND PULocationID < 10 AND DOLocationID = 1;
```

### InnoDB
```
select count(DOLocationID) from `nyc_yellow_taxi_innodb_zlib` where tpep_pickup_datetime between '2016-07-31 20:31:45.000000' AND '2018-01-01 00:00:00.000000' AND PULocationID > 1 AND PULocationID < 10 AND DOLocationID = 1;
```

### MyRocks
```
select count(DOLocationID) from `nyc_yellow_taxi_myrocks` where tpep_pickup_datetime between '2016-07-31 20:31:45.000000' AND '2018-01-01 00:00:00.000000' AND PULocationID > 1 AND PULocationID < 10 AND DOLocationID = 1;
```