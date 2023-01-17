File Source : https://data.govt.in


Steps to transfer data from local storage to Hive:

1. Copy csv file from local storage to hdfs :
knull@LAPTOP-J5UEVEDO:~$ hadoop fs -copyFromLocal /home/knull/karthikesavan/Airlines.csv /user/storage/Airlines/Airlines.csv

2. Copy the column names from csv files, to create table in hive.
   For that view the csv using 'cat' command.
knull@LAPTOP-J5UEVEDO:~$ hadoop fs -cat /user/storage/Airlines/Airlines.csv

Category,SL_No,AIRLINE_NAME,JANUARY_PASSENGERS_TO_INDIA,JANUARY_PASSENGERS_FROM_INDIA,JANUARY_FREIGHT_TO_INDIA,JANUARY_FREIGHT_FROM_INDIA,FEBRUARY_PASSENGERS_TO_INDIA,FEBRUARY_PASSENGERS_FROM_INDIA,FEBRUARY_FREIGHT_TO_INDIA,FEBRUARY_FREIGHT_FROM_INDIA,MARCH_PASSENGERS_TO_INDIA,MARCH_PASSENGERS_FROM_INDIA,MARCH_FREIGHT_TO_INDIA,MARCH_FREIGHT_FROM_INDIA
---------------------------------------------------
---------------------------------------------------

3. Start Hive query engine.
knull@LAPTOP-J5UEVEDO:~$ hive

4. Create database and table :
   create database project;
   hive> create table project.airlines
       > (Category string,SL_No int,AIRLINE_NAME string,
       > JANUARY_PASSENGERS_TO_INDIA int,JANUARY_PASSENGERS_FROM_INDIA int,JANUARY_FREIGHT_TO_INDIA decimal,JANUARY_FREIGHT_FROM_INDIA decimal,
       > FEBRUARY_PASSENGERS_TO_INDIA int,FEBRUARY_PASSENGERS_FROM_INDIA int,FEBRUARY_FREIGHT_TO_INDIA decimal,FEBRUARY_FREIGHT_FROM_INDIA decimal,
       > MARCH_PASSENGERS_TO_INDIA int,MARCH_PASSENGERS_FROM_INDIA int,MARCH_FREIGHT_TO_INDIA decimal,MARCH_FREIGHT_FROM_INDIA decimal)
       > ROW FORMAT DELIMITED 
       > FIELDS TERMINATED BY ','
       > LINES TERMINATED BY '\n'
       > STORED AS TEXTFILE
       > TBLPROPERTIES("skip.header.line.count"="1");

5. Load table into hive :
   hive> LOAD DATA INPATH '/user/storage/Airlines/Airlines.csv' INTO TABLE project.airlines;
   

