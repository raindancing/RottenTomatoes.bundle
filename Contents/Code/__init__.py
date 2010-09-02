#Rotten Tomatoes
RT_SEARCH_URL = 'http://www.rottentomatoes.com/search/full_search.php?search=%s'
RT_BASE_URL   = 'http://www.rottentomatoes.com'

def Start():
  HTTP.CacheTime = CACHE_1DAY
  
class RottenTomatoesAgent(Agent.Movies):
  name = 'Rotten Tomatoes'
  languages = [Locale.Language.English]
  primary_provider = False
  contributes_to = ['com.plexapp.agents.imdb']
  
  def search(self, results, media, lang):
    rtSearchResult = HTML.ElementFromURL(RT_SEARCH_URL % str(media.primary_metadata.id).replace('tt','')).xpath('//td[contains(@class,"firstCol") and @width="85%"]')
    if len(rtSearchResult) > 0:
      rtMovieUrl = rtSearchResult[0].xpath('p/a')[0].get('href')
      #Log("**" + rtMovieUrl)
      results.Append(
        MetadataSearchResult(
          id    = rtMovieUrl,
          score = 100
        )    
      )
    
  def update(self, metadata, media, lang):
    #load the rt movie page and grab the ratings
    ratings = {}
    for rating in HTML.ElementFromURL(RT_BASE_URL + metadata.id).xpath('//div[@class="movie_info_area"]//li/a'):
      ratingText = rating.get('title')
      if ratingText != "N/A" and len(ratingText) > 0:
        ratings[rating.xpath('span')[0].text] = float(ratingText.replace('%',''))/10
    metadata.rating = ratings['T-Meter Critics']
    
    