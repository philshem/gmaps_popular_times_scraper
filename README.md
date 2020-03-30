# Scraper of Google Maps "Popular Times" for business entries

Turn this:

![screenshot of google maps popular times](https://gist.githubusercontent.com/philshem/71507d4e8ecfabad252fbdf4d9f8bdd2/raw/ab2530b4b3bfab57f4fe65ddc58792f4bb76758e/gmaps_popular_times.png)

into a machine readable dataset. (This is really unofficial. YMMV.)

## to get the code

    git clone https://github.com/philshem/gmaps_popular_times_scraper.git
    cd gmaps_popular_times_scraper

## to configure the code

Install required packages ([selenium](https://pypi.org/project/selenium/) and [beautifulsoup4](https://pypi.org/project/beautifulsoup4/))

    pip3 install -r requirements.txt

Modify these lines in the code `config.py` to point to your path of Chrome and chromedriver.

    CHROME_BINARY_LOCATION = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    CHROMEDRIVER_BINARY_LOCATION = '/usr/local/bin/chromedriver'

Chromedriver downloads are [here](https://sites.google.com/a/chromium.org/chromedriver/downloads). Make sure you use the version that matches your Chrome version.

## to run the code

Run the scraper by putting a URL as the system argument:

    python3 scrape_gm.py "$URL_TO_CSV"

or specifically for a list of URLs stored in a google sheet

    python3 scrape_gm.py "https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

The URL should point to any CSV (local or http) that has as the first column a valid google maps url.
For example, a valid google maps URL:

    https://www.google.com/maps/place/Der+Gr%C3%BCne+Libanon/@47.3809042,8.5325368,17z/data=!3m1!4b1!4m5!3m4!1s0x47900a0e662015b7:0x54fec14b60b7f528!8m2!3d47.3809006!4d8.5347255

Or a shortened one is also valid:

    https://goo.gl/maps/r2xowUB3UZX7ZL2u6

Note that the html page source can be saved to the folder `html/` by setting the parameter in `config.py`. If the html files are saved as cache, with a timestamp for when they were retrieved, and can be cleaned out once in a while. Logs are saved to `logs/`, which makes an archive of the URLs retrieved based on the CSV input file.

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

All technical timestamps, for example `20200318_163629`, are in the machine's time. The hour from the column `hour_of_day` is in the local time of the mapped place.

Data in csv format is saved to `data/`. You can use the code ([csv2sql.py](https://raw.githubusercontent.com/philshem/gmaps_popular_times_scraper/master/csv2sql.py)) to convert to a SQLite3 database. Or this [awk command](https://stackoverflow.com/a/40922632/2327328) to take all individual CSVs for each place and time, and write to one big CSV called `all.csv`

    awk 'FNR==NR||FNR>2' data/*.csv > all.csv

## dataviz

And to visualize the data for a week of one Kebab shop in Zürich (note that Friday at 12 is max crowd!)

![shawarma popularity](https://gist.githubusercontent.com/philshem/71507d4e8ecfabad252fbdf4d9f8bdd2/raw/ab2530b4b3bfab57f4fe65ddc58792f4bb76758e/shawarma_popularity.png)


## other

upload to public bucket

```
cd /home/philip/gmaps_popular_times_scraper
# upload all raw csvs to bucket
gsutil -m cp -n data/*.csv gs://kantonzh-covid-hkfsaqgshw/gmaps_scrape/raw_data/

# concat all csv files into one big one, upload to bucket
awk 'FNR==NR||FNR>2' data/*.csv > all.csv && gsutil -m cp all.csv gs://kantonzh-covid-hkfsaqgshw/gmaps_scrape/

# from that big csv, only print lines that do not end with a comma, which are valid for comparing actual and current
# and upload to bucket
awk '!/[,]$/' all.csv > all_valid.csv && gsutil -m cp all_valid.csv gs://kantonzh-covid-hkfsaqgshw/gmaps_scrape/
```

run script

```
cd /home/philip/gmaps_popular_times_scraper
/usr/bin/python3 scrape_gm.py "https://docs.google.com/spreadsheets/d/1KDqquW2axaUM9Z62JbyppuPq09IpAZRSIpPLb08nVqQ/gviz/tq?tqx=out:csv&sheet=Sheet1" >> out.log
```

crontab

```
30 * * * * /home/philip/gmaps_popular_times_scraper/./run.sh >> /home/philip/gmaps_popular_times_scraper/cron.log
00 * * * * /home/philip/gmaps_popular_times_scraper/./upload.sh >> /home/philip/gmaps_popular_times_scraper/cron_upload.log
```