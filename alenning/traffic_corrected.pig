traffic = LOAD 'hdfs://simplex1:9000/user/pdotson/Traffic_large_corrected_pig.csv' USING PigStorage(',') as (ViolationType:chararray, Gender:chararray, Race:chararray, VehicleType:chararray, Color:chararray, State:chararray, DLState:chararray);

foreach_gender = FOREACH traffic GENERATE Gender;

gender_dist = DISTINCT foreach_gender;

DUMP gender_dist;

traffic_by_gender = GROUP traffic BY Gender;

count_gender = FOREACH traffic_by_gender GENERATE COUNT(traffic);

DUMP count_gender;

foreach_race = FOREACH traffic GENERATE Race;

race_dist = DISTINCT foreach_race;

DUMP race_dist;

traffic_by_race = GROUP traffic by Race;

count_race = FOREACH traffic_by_race GENERATE COUNT(traffic);

DUMP count_race;
