#!/bin/bash

e=
for (( i = 5; i >= 0; i-- )) ; do
    e='-e /'`date +\%R -d "-$i min"`'/p '$e
done

$(sed -n $e /path/to/user/home/csvdata/siamining_hashrate.csv > /path/to/user/home/csvdata_tmp/siamining_hashrate.csv)
$(sed -n $e /path/to/user/home/csvdata/ahashpool_hashrate.csv > /path/to/user/home/csvdata_tmp/ahashpool_hashrate.csv)
$(sed -n $e /path/to/user/home/csvdata/ahashpool_profit.csv > /path/to/user/home/csvdata_tmp/ahashpool_profit.csv)
$(sed -n $e /path/to/user/home/csvdata/blazepool_hashrate.csv > /path/to/user/home/csvdata_tmp/blazepool_hashrate.csv)
$(sed -n $e /path/to/user/home/csvdata/blazepool_profit.csv > /path/to/user/home/csvdata_tmp/blazepool_profit.csv)
$(sed -n $e /path/to/user/home/csvdata/zpool_hashrate.csv > /path/to/user/home/csvdata_tmp/zpool_hashrate.csv)
$(sed -n $e /path/to/user/home/csvdata/zpool_profit.csv > /path/to/user/home/csvdata_tmp/zpool_profit.csv)
$(sed -n $e /path/to/user/home/csvdata/bitminter_hashrate.csv > /path/to/user/home/csvdata_tmp/bitminter_hashrate.csv)
$(sed -n $e /path/to/user/home/csvdata/hashrefinery_hashrate.csv > /path/to/user/home/csvdata_tmp/hashrefinery_hashrate.csv)
$(sed -n $e /path/to/user/home/csvdata/hashrefinery_profit.csv > /path/to/user/home/csvdata_tmp/hashrefinery_profit.csv)

mysql -u username -pPassword database <<MY_QUERY

LOAD DATA LOCAL INFILE '/path/to/user/home/csvdata_tmp/siamining_hashrate.csv' INTO TABLE siamining_hashrate FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INFILE '/path/to/user/home/csvdata_tmp/ahashpool_hashrate.csv' INTO TABLE ahashpool_hashrate FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INFILE '/path/to/user/home/csvdata_tmp/ahashpool_profit.csv' INTO TABLE ahashpool_profit FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INFILE '/path/to/user/home/csvdata_tmp/blazepool_hashrate.csv' INTO TABLE blazepool_hashrate FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INFILE '/path/to/user/home/csvdata_tmp/blazepool_profit.csv' INTO TABLE blazepool_profit FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INFILE '/path/to/user/home/csvdata_tmp/zpool_hashrate.csv' INTO TABLE zpool_hashrate FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INFILE '/path/to/user/home/csvdata_tmp/zpool_profit.csv' INTO TABLE zpool_profit FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INFILE '/path/to/user/home/csvdata_tmp/bitminter_hashrate.csv' INTO TABLE bitminter_hashrate FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INFILE '/path/to/user/home/csvdata_tmp/hashrefinery_hashrate.csv' INTO TABLE hashrefinery_hashrate FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INFILE '/path/to/user/home/csvdata_tmp/hashrefinery_profit.csv' INTO TABLE hashrefinery_profit FIELDS TERMINATED BY ',';
MY_QUERY

