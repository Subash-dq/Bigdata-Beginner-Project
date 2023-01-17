create table domestic
    (SL_No int,
    AIRLINE_NAME string,
    JANUARY_PASSENGERS_TO_INDIA int,
    FEBRUARY_PASSENGERS_TO_INDIA int)
    partitioned by (Category string);


insert into table domestic partition (Category='domestic carriers') 
    select SL_No,AIRLINE_NAME,JANUARY_PASSENGERS_TO_INDIA,FEBRUARY_PASSENGERS_TO_INDIA 
    from airlines 
    where Category='DOMESTIC CARRIERS';