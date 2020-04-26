# web-scraping-challenge

Our challenge was to scrape information from five different websites to gather data related to Mars as follows:

1) Scrape the [NASA Mars News Site](https://mars.nasa.gov/news/) and collect the latest News Title and Paragraph Text.
2) Visit the url for JPL Featured Space Image [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars) and retrieve the full sized featured image.
3) Visit the Mars Weather twitter account [here](https://twitter.com/marswxreport?lang=en) and scrape the latest Mars weather tweet from the page.
4) Visit the Mars Facts webpage [here](https://space-facts.com/mars/) and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
5) Visit the USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution images for each of Mar's hemispheres.

After scraping each of the five websites, we used MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs above.

The screenshot of my HTML page is displayed below:
