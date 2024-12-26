import xml.etree.ElementTree as ET
from .Logger import logger
import requests,time,ssl

def parsefeeds(rss_url):
    try:
        response = requests.get(rss_url)
        time.sleep(5)
        if response.ok:
            root = ET.fromstring(response.content)
            feeds_list = []
            feeds_obj = {}
            for item in root.iter("item"):
                creator = item.find("dc:creator", {'dc': 'http://purl.org/dc/elements/1.1/'})
                author = creator.text if creator is not None else "Unknown"
                title = item.find("title").text
                link = item.find("link").text
                published = item.find("pubDate").text
                tags = item.findall("category")
                tag_list = []
                if tags != []:
                    for tag in tags:
                        tag_list.append(tag.text)
                else:
                    tag_list = []
                feeds_obj = {"author": author, "title": title, "url": link, "published": published, "tags": tag_list}
                feeds_list.append(feeds_obj)
            logger("{} fetched".format(rss_url), "INF")
            return feeds_list
                
        else:
            logger("Error while fetching feeds response : {}".format(response), "ERR")
            logger("Url : {}".format(rss_url), "ERR")
            return []

    except Exception as e:

        logger("Error while fetching feeds Url : {}".format(rss_url), "ERR")



def scrape(urls):
    try:
        objects = []
        logger("Loading New Feeds ...", "INF")

        if hasattr(ssl, '_create_unverified_context'):
            ssl._create_default_https_context = ssl._create_unverified_context

        for url in urls:
            feeds = parsefeeds(url)
            if feeds != [] and feeds != None:
                for feed in feeds:
                    if feed not in objects:
                        objects.append(feed)
        logger("New Feeds loaded Successfully", "OK")
        return objects

    except Exception as e:
        logger("Error : "+str(e), "ERR")
        exit(1)
