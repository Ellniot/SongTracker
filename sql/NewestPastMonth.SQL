SELECT song_name,artist_name FROM the_current 
WHERE timestamp > (
	SELECT date('now','-1 month')
)
AND timestamp < (
	SELECT date('now')
)
ORDER BY timestamp DESC LIMIT 3