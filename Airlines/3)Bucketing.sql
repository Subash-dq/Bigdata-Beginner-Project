set hive.exec.dynamic.partition=true;
set hive.exec.dynamic.partition.mode=nonstrict;
set hive.enforce.bucketing = true;

-- create table before bucketing
create table airlines
  (Category string,SL_No int,AIRLINE_NAME string,
  JANUARY_PASSENGERS_TO_INDIA int,JANUARY_PASSENGERS_FROM_INDIA int,JANUARY_FREIGHT_TO_INDIA decimal,JANUARY_FREIGHT_FROM_INDIA decimal,
  FEBRUARY_PASSENGERS_TO_INDIA int,FEBRUARY_PASSENGERS_FROM_INDIA int,FEBRUARY_FREIGHT_TO_INDIA decimal,FEBRUARY_FREIGHT_FROM_INDIA decimal,
  MARCH_PASSENGERS_TO_INDIA int,MARCH_PASSENGERS_FROM_INDIA int,MARCH_FREIGHT_TO_INDIA decimal,MARCH_FREIGHT_FROM_INDIA decimal)
  ROW FORMAT DELIMITED 
  FIELDS TERMINATED BY ','
  LINES TERMINATED BY '\n'
  STORED AS TEXTFILE
  TBLPROPERTIES("skip.header.line.count"="1");

LOAD DATA INPATH '/user/storage/Airlines/Airlines.csv' INTO TABLE project.airlines;

-- create BUCKETING TABLE

create table bk_airlines(
    AIRLINE_NAME string,
    JANUARY_PASSENGERS_TO_INDIA int,
    FEBRUARY_PASSENGERS_TO_INDIA int)
    COMMENT 'Bucket table for Airlines' 
    CLUSTERED BY (JANUARY_PASSENGERS_TO_INDIA) INTO 3 BUCKETS STORED AS textfile;

insert into table bk_airlines
    select avg(JANUARY_PASSENGERS_TO_INDIA) 
    FROM bk_airlines TABLESAMPLE(BUCKET 1 OUT OF 3 ON JANUARY_PASSENGERS_TO_INDIA) s;

insert into table bk_airlines
    select avg(JANUARY_PASSENGERS_TO_INDIA) 
    FROM bk_airlines TABLESAMPLE(BUCKET 1 OUT OF 3 ON rand()) s;