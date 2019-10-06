import requests
import json
import sys
import time
from bs4 import BeautifulSoup

MAX_PAGE_NUM = 700
HOST = "www.kickstarter.com/discover/categories/"
CATEGORIES = ["art",
              "comics",
              "crafts",
              "dance",
              "design",
              "fashion",
              "film%20&%20video",
              "food",
              "games",
              "journalism",
              "music",
              "photography",
              "publishing",
              "technology",
              "theater"]


def save_article(url_article):
    filename = url_article.split("/")[-1] + ".json"
    article = dict()
    try:
        response = requests.get(url_article)
        soup = BeautifulSoup(response.text, "html.parser")
        body = soup.find("body")
        # menu_horizontal = content.find("div", {"class": "grid-container flex flex-column"})
        # names = menu_horizontal.findAll("span", {"class": "ml1"})
        # place = names[-1].getText()
        # links = menu_horizontal.findAll("a", {
        #     "class": "nowrap navy-700 flex items-center medium mr3 type-12 keyboard-focusable"})
        # category = links[-2]["href"]
        content = body.find("div", {"id": "content-wrap"})
        menu_vertical = content.find("div", {"class": "bg-grey-100"})
        data = json.loads(menu_vertical["data-initial"])["project"]
        article["id"] = data["id"]
        article["url"] = url_article
        article["name"] = soup.find("meta", {"property": "og:title"})["content"]
        article["description"] = soup.find("meta", {"property": "og:description"})["content"]
        article["deadlineAt"] = data["deadlineAt"]
        article["backersCount"] = data["backersCount"]
        article["pledged"] = data["pledged"]
        article["goal"] = data["goal"]
        article["location"] = data["location"]["displayableName"]
        article["isProjectWeLove"] = data["isProjectWeLove"]
        article["subcategory"] = data["category"]["name"]
        article["category"] = data["category"]["parentCategory"]["name"]
        about = body.find("div", {"class": "rte__content js-full-description responsive-media"}).findAll("p")
        article["about"] = [paragraf.text for paragraf in about]
        risks_and_challenges = body.find("div", {"class": "mb3 mb10-sm mb3 js-risks"}).findAll("p")
        article["risksAndChallenges"] = [paragraf.text for paragraf in risks_and_challenges]
    except:
        article["error"] = str(sys.exc_info()[1])
        print(article["error"])
        filename = "error " + filename
        time.sleep(5)
    finally:
        with open("data/" + filename, "w") as json_file:
            json.dump(article, json_file)


def run(category):
    for i in range(1, MAX_PAGE_NUM + 1):
        url_explore = HOST + category + "?page=" + str(i)
        print(url_explore)
    # save_article(url_article)


run(CATEGORIES[0])
