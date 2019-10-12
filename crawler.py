import requests
import json
import time
from bs4 import BeautifulSoup
import traceback
from datetime import datetime


def save_project(url_project):
    filename = url_project.split("/")[-1] + ".json"
    project = dict()

    try:
        response = requests.get(url_project)
        soup = BeautifulSoup(response.text, "html.parser")

        script = soup.findAll('script')[2]
        current_project = script.text \
            .split("window.current_project = \"")[1] \
            .split("\";\n")[0] \
            .replace("\\\\&quot", "") \
            .replace("&quot;", "\"")
        data = json.loads(current_project)

        project["url"] = url_project
        project["title"] = soup.find("meta", {"property": "og:title"})["content"]
        project["description"] = soup.find("meta", {"property": "og:description"})["content"]
        project["state"] = data["state"]
        project["createdAt"] = datetime.fromtimestamp(data["created_at"]).strftime('%Y-%m-%d %H:%M:%S')
        project["deadlineAt"] = datetime.fromtimestamp(data["deadline"]).strftime('%Y-%m-%d %H:%M:%S')
        project["backersCount"] = data["backers_count"]
        project["currency"] = data["currency"]
        project["pledged"] = data["pledged"]
        project["pledgedUSD"] = float(data["usd_pledged"])
        project["goal"] = data["goal"]
        project["location"] = data["location"]["name"]
        project["country"] = data["location"]["country"]
        project["creator"] = data["creator"]["name"]
        project["category"] = data["category"]["slug"].split("/")

        body = soup.find("body")

        about_list = body.find("div", {"class": "rte__content js-full-description responsive-media"})
        if about_list is not None:
            about = about_list.findAll("p")
            project["about"] = ' '.join([str(paragraph.text) for paragraph in about])

        risks_and_challenges_list = body.find("div", {"class": "mb3 mb10-sm mb3 js-risks"})
        if risks_and_challenges_list is not None:
            risks_and_challenges = risks_and_challenges_list.findAll("p")
            project["risksAndChallenges"] = ' '.join([str(paragraph.text) for paragraph in risks_and_challenges])
    except:
        project["error"] = str(traceback.format_exc())
        print(project["error"])
        filename = "error " + filename
        time.sleep(5)
    finally:
        # print(print(json.dumps(project, indent=4, sort_keys=True)))
        with open("data/" + filename, "w", encoding="utf8") as json_file:
            json.dump(project, json_file, indent=4, ensure_ascii=False)


def seek_category(host, logger, max_page_num=200):
    project_id = 1
    for page_id in range(1, max_page_num + 1):
        url_explore = host + "&page=" + str(page_id)

        response = requests.get(url_explore)
        soup = BeautifulSoup(response.text, "html.parser")

        body = soup.find("body")
        projects_rows = body.find("div", {"id": "projects_list"}) \
            .findAll("div", {"class": "grid-row flex flex-wrap"})

        projects = list()
        for row in projects_rows:
            projects.extend(row.findAll("div",
                                        {"class": "js-react-proj-card grid-col-12 grid-col-6-sm grid-col-4-lg"}))

        if len(projects) == 0:
            break

        for project_data in [project["data-project"] for project in projects]:
            url_project = json.loads(project_data)["urls"]["web"]["project"]
            logger.write(str(project_id) + "," + str(page_id) + "," + url_project + "\n")
            print(str(project_id) + "," + str(page_id) + "," + url_project)
            save_project(url_project)
            project_id = project_id + 1
            time.sleep(1)
        time.sleep(1)


if __name__ == "__main__":
    HOST = "https://www.kickstarter.com/discover/advanced"
    category_list = [20, 21, 22, 23, 24, 25, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45,
                     46, 47, 48, 49, 50, 51, 52, 53, 54, 239, 241, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272,
                     273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292,
                     293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312,
                     313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332,
                     333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352,
                     353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 386]
    for category_id in category_list:  # in range(10, 500):
        with open("logs/category_" + str(category_id) + ".csv", "w") as logger:
            # response = requests.get(HOST + "?category_id=" + str(category_id) + "&page=1")
            # soup = BeautifulSoup(response.text, "html.parser")
            #
            # title = soup.find("title").text
            # if title == "The page you were looking for doesn't exist (404)":
            #     pass
            #     logger.write("The page you were looking for doesn't exist (404)\n")
            # elif len(title[12:][:-15].split(" / ")) == 1:
            #     pass
            #     logger.write("Subcategory is empty\n")
            # else:
            seek_category(HOST + "?category_id=" + str(category_id), logger, 1)
            break


# # TEST__________________________________________________________________________________________________________________
# if __name__ == "__main__":
#     url_LIVE = "https://www.kickstarter.com/projects/stencilbydonnybrook/the-stencil-by-donny-brook"
#     save_project(url_LIVE)
#     url_DEATH = "https://www.kickstarter.com/projects/170839637/rain-painting-trip-to-seattle"
#     save_project(url_DEATH)
# # TEST__________________________________________________________________________________________________________________