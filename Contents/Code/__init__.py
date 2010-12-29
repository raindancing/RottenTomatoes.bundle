RT_IMDB_SEARCH_URL = 'http://www.rottentomatoes.com/alias?type=imdbid&s=%s'

def Start():
	HTTP.CacheTime = CACHE_1DAY

class RottenTomatoesAgent(Agent.Movies):
	name = 'Rotten Tomatoes'
	languages = [Locale.Language.English]
	primary_provider = False
	contributes_to = ['com.plexapp.agents.imdb']

	def search(self, results, media, lang):
		imdb_id = media.primary_metadata.id.replace('tt', '')
		results.Append(MetadataSearchResult(id=imdb_id, score=100))

	def update(self, metadata, media, lang):
		movie_page = HTML.ElementFromURL(RT_IMDB_SEARCH_URL % metadata.id)
		# Rating
		try:
			avg_rating = movie_page.xpath('//div[@id="all-critics-numbers"]/div/p/span')[0].text.split('/')[0]
			metadata.rating = float(avg_rating)
		except:
			pass

		# Summary
		try:
			metadata.summary = movie_page.xpath('//span[@id="movie_synopsis_all"]')[0].text
		except:
			pass

		# Genres
		metadata.genres.clear()
		try:
			for genre_elem in movie_page.xpath('//span[@property="v:genre"]'):
				metadata.genres.add(genre_elem.text)
		except:
			pass
