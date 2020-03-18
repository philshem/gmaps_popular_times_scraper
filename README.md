# Scraper of Google Maps "Popular Times" for business entries

Turn this:

![screenshot of google maps popular times](https://gist.githubusercontent.com/philshem/71507d4e8ecfabad252fbdf4d9f8bdd2/raw/ab2530b4b3bfab57f4fe65ddc58792f4bb76758e/gmaps_popular_times.png)

into a machine readable dataset. (This is really unofficial. YMMV.)

## to get the code

    git clone https://github.com/philshem/gmaps_popular_times_scraper.git
    cd gmaps_popular_times_scraper

Install required packages ([selenium](https://pypi.org/project/selenium/) and [beautifulsoup4](https://pypi.org/project/beautifulsoup4/))

    pip3 install -r requirements.txt

Modify these lines in the code `scrape_gm.py` to point to your path of Chrome and chromedriver.

    options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    chrome_driver_binary = "/usr/local/bin/chromedriver"

Chromedriver downloads are [here](https://sites.google.com/a/chromium.org/chromedriver/downloads). Make sure you use the version that matches your Chrome.

## to run the code

Run the scraper by putting a URL as the system argument:

    python3 scrape_gm.py "$URL_TO_CSV"

or specifically for a google sheets

    python scrape_gm.py "https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

The URL should point to any CSV (local or http) that has as the first column a valid google maps url.
For example:

    https://www.google.com/maps/place/Der+Gr%C3%BCne+Libanon/@47.3809042,8.5325368,17z/data=!3m1!4b1!4m5!3m4!1s0x47900a0e662015b7:0x54fec14b60b7f528!8m2!3d47.3809006!4d8.5347255

Or a shortened one:

    https://goo.gl/maps/r2xowUB3UZX7ZL2u6

Note that the html page source will be saved to the folder `html/`. The html files are saved as an cache, with a timestamp for when they were retrieved, and should be cleaned out once in a while. Logs are saved to `logs/`.

## results

The output data ([sample_output.csv](https://raw.githubusercontent.com/philshem/gmaps_popular_times_scraper/master/sample_output.csv)) has this structure (abbreviated):

```
place,url,scrape_time,day_of_week,hour_of_day,popularity_percent_normal,popularity_percent_current
AnRYn1F8NfSGLexf7,https://goo.gl/maps/AnRYn1F8NfSGLexf7,20200318_163629,Wednesday,13,38,
AnRYn1F8NfSGLexf7,https://goo.gl/maps/AnRYn1F8NfSGLexf7,20200318_163629,Wednesday,14,45,
AnRYn1F8NfSGLexf7,https://goo.gl/maps/AnRYn1F8NfSGLexf7,20200318_163629,Wednesday,15,61,
AnRYn1F8NfSGLexf7,https://goo.gl/maps/AnRYn1F8NfSGLexf7,20200318_163629,Wednesday,16,79,30
AnRYn1F8NfSGLexf7,https://goo.gl/maps/AnRYn1F8NfSGLexf7,20200318_163629,Wednesday,17,90,
AnRYn1F8NfSGLexf7,https://goo.gl/maps/AnRYn1F8NfSGLexf7,20200318_163629,Wednesday,18,88,
```

Data in csv format is saved to `data/`. You can use the code ([csv2sql.py](https://raw.githubusercontent.com/philshem/gmaps_popular_times_scraper/master/csv2sql.py)) to convert to a SQLite3 database. Or this [awk command](https://stackoverflow.com/a/40922632/2327328)

    awk 'FNR==NR||FNR>2' data/*.csv > all.csv

## dataviz

And to visualize the data for a week of one Kebab shop in Zürich (note that Friday at 12 is max crowd!)

![shawarma popularity](https://gist.githubusercontent.com/philshem/71507d4e8ecfabad252fbdf4d9f8bdd2/raw/ab2530b4b3bfab57f4fe65ddc58792f4bb76758e/shawarma_popularity.png)

