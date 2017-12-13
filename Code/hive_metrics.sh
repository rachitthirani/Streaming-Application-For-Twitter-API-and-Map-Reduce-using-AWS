DATE=$(date +"%Y%m%d_%H%M%S")

LOGFILE="./"$DATE".log"

echo "Executing hive script " >> $LOGFILE

START1=$(date +%s);

hive -f ./hive.hql

END1=$(date +%s);

echo "hive.hql" 

echo $((END1-START1)) | awk '{print int($1/60)":"int($1%60)}'

echo "Hive process is done";

exit;
