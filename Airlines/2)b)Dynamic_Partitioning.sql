create table categories
    (SL_No int,
    AIRLINE_NAME string,
    JANUARY_PASSENGERS_TO_INDIA int,
    FEBRUARY_PASSENGERS_TO_INDIA int)
    partitioned by (Category string);

set hive.exec.dynamic.partition.mode=nonstrict;

insert into table categories (Category) 
    select SL_No,AIRLINE_NAME,JANUARY_PASSENGERS_TO_INDIA,FEBRUARY_PASSENGERS_TO_INDIA,CATEGORY
    from airlines 
    where Category='FOREIGN CARRIERS';

