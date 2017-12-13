input_lines = LOAD 'hdfs:///twitter/000000_0' AS (name:chararray);
 
 -- Extract words from each line and put them into a pig bag
 -- datatype, then flatten the bag to get one word on each row
 filtered_names = FOREACH input_lines GENERATE FLATTEN(TOKENIZE(name)) AS name;
 --filtered_names = FOREACH names GENERATE STRSPLIT(name,' ',1) as name;
 --dump names;
 
-- filter out any words that are just white spaces
 --filtered_names = FILTER names BY name MATCHES '\\w+';
 
 --dump filtered_names;
 -- create a group for each word
 name_groups = GROUP filtered_names BY name;
 
 --dump name_groups;
 -- count the entries in each group
 name_count = FOREACH name_groups GENERATE COUNT(filtered_names) AS count, group AS name;
 
 -- order the records by count
 ordered_name_count = ORDER name_count BY count DESC;
 --DUMP ordered_name_count;
 STORE ordered_name_count INTO 'hdfs:///twitter/name_count';
