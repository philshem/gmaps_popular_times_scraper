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

## to run the code

Run the scraper by putting a URL as the system argument:

    python3 scrape_gm.py $URL

The URL can be a full google maps URL

    https://www.google.com/maps/place/Der+Gr%C3%BCne+Libanon/@47.3809042,8.5325368,17z/data=!3m1!4b1!4m5!3m4!1s0x47900a0e662015b7:0x54fec14b60b7f528!8m2!3d47.3809006!4d8.5347255

Or a shortened one:

    https://goo.gl/maps/r2xowUB3UZX7ZL2u6

Note that the html page source will be saved to the folder `html/`

## results

The output data ([sample_output.csv](https://raw.githubusercontent.com/philshem/gmaps_popular_times_scraper/master/sample_output.csv)) has this structure (abbreviated):

```
Der_Grüne_Libanon,Sunday,6,0
Der_Grüne_Libanon,Sunday,7,0
Der_Grüne_Libanon,Sunday,8,0
Der_Grüne_Libanon,Sunday,9,0
Der_Grüne_Libanon,Sunday,10,1
Der_Grüne_Libanon,Sunday,11,10
Der_Grüne_Libanon,Sunday,12,33
Der_Grüne_Libanon,Sunday,13,61
Der_Grüne_Libanon,Sunday,14,69
Der_Grüne_Libanon,Sunday,15,50
Der_Grüne_Libanon,Sunday,16,38
Der_Grüne_Libanon,Sunday,17,53
Der_Grüne_Libanon,Sunday,18,55
Der_Grüne_Libanon,Sunday,19,27
Der_Grüne_Libanon,Sunday,20,0
Der_Grüne_Libanon,Sunday,21,0
Der_Grüne_Libanon,Sunday,22,0
Der_Grüne_Libanon,Sunday,23,0
...
Der_Grüne_Libanon,Saturday,6,0
Der_Grüne_Libanon,Saturday,7,0
Der_Grüne_Libanon,Saturday,8,0
Der_Grüne_Libanon,Saturday,9,0
Der_Grüne_Libanon,Saturday,10,3
Der_Grüne_Libanon,Saturday,11,19
Der_Grüne_Libanon,Saturday,12,56
Der_Grüne_Libanon,Saturday,13,76
Der_Grüne_Libanon,Saturday,14,64
Der_Grüne_Libanon,Saturday,15,57
Der_Grüne_Libanon,Saturday,16,58
Der_Grüne_Libanon,Saturday,17,53
Der_Grüne_Libanon,Saturday,18,41
Der_Grüne_Libanon,Saturday,19,26
Der_Grüne_Libanon,Saturday,20,0
Der_Grüne_Libanon,Saturday,21,0
Der_Grüne_Libanon,Saturday,22,0
Der_Grüne_Libanon,Saturday,23,0
```

## dataviz

And to visualize the data for a week of one Kebab shop in Zürich (note that Friday at 12 is max crowd!)

![shawarma popularity](https://gist.githubusercontent.com/philshem/71507d4e8ecfabad252fbdf4d9f8bdd2/raw/ab2530b4b3bfab57f4fe65ddc58792f4bb76758e/shawarma_popularity.png)

