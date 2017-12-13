SELECT word, count(1) AS count FROM
 (SELECT explode(split(name, '\\s')) AS word FROM twitter_hdfs) temp
GROUP BY word
ORDER BY count;
