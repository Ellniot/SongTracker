SELECT song_name, artist_name, COUNT(song_name||artist_name) AS cnt
FROM the_current_test
GROUP BY song_name
ORDER BY cnt DESC 
LIMIT 10