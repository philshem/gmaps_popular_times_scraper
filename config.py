import os

# give time to download map tiles
SLEEP_SEC = 20.0

# csv output delimiter
DELIM = ','
HEADER_COLUMNS = ('place', 'url', 'scrape_time', 'day_of_week', 'hour_of_day', 'popularity_percent_normal', 'popularity_percent_current')

# keep an cache of the source htmls, with a timestamp in the filename
# if so, they should be cleaned out once in a while, since they are 1MB each
SAVE_HTML = True

# put your url or path here to a csv where the first column is a google maps url
# google sheets - export as csv https://stackoverflow.com/a/33727897/2327328
URL_PATH_INPUT = None
#URL_PATH_INPUT = 'urls.csv'

DEBUG = False
URL_PATH_INPUT_TEST = 'tests' + os.sep + 'test_urls.csv'