--- Seems to only count the ones in the last month... not sure tho ---
SELECT song_name, artist_name, COUNT(song_name||artist_name) AS cnt
FROM the_current_test
WHERE timestamp > (
	SELECT date('now','+1 month')
)
GROUP BY song_name
ORDER BY cnt DESC 
LIMIT 10