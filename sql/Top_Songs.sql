/* Seems to only count the ones in the last month... not sure tho */
/*  s #1 should be the desired table name (the radio station)
	d #1 should be the # of past months to include
	d #2 should be the number of desired results  */
SELECT song_name, artist_name, COUNT(song_name||artist_name) AS cnt
FROM %s
WHERE timestamp > (
	SELECT date('now','-%d month')
)
GROUP BY song_name
ORDER BY cnt DESC
LIMIT %d