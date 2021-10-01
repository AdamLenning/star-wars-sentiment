traffic = LOAD 'hdfs://simplex1:9000/user/alenning/Traffic_large.csv' USING PigStorage(',') as (ViolationType:chararray, Gender:chararray, Race:chararray, VehicleType:chararray, Color:chararray, State:chararray, DLState:chararray, DateOfStop:chararray);

Group_data = GROUP traffic  BY (Gender, ViolationType);

DUMP Group_data; 
