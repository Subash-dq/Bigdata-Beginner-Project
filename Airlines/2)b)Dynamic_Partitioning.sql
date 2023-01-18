-- create and load table before partitioning

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


-- create PARTITION TABLE 

set hive.exec.dynamic.partition.mode=nonstrict;

create table domestic
    (SL_No int,
    AIRLINE_NAME string,
    JANUARY_PASSENGERS_TO_INDIA int,
    FEBRUARY_PASSENGERS_TO_INDIA int)
    partitioned by (Category string);

insert into table categories (Category) 
    select SL_No,AIRLINE_NAME,JANUARY_PASSENGERS_TO_INDIA,FEBRUARY_PASSENGERS_TO_INDIA,CATEGORY
    from airlines 
    where Category='FOREIGN CARRIERS';

