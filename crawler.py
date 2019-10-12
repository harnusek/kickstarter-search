import requests
import json
import time
from bs4 import BeautifulSoup
import traceback
from datetime import datetime


def save_project(url_project):
    status = True
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
        if "location" in data:
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
        status = False
    finally:
        # print(print(json.dumps(project, indent=4, sort_keys=True)))
        with open("data/" + filename, "w", encoding="utf8") as json_file:
            json.dump(project, json_file, indent=4, ensure_ascii=False)
        return status


def seek_projects(host, logger, max_page_num=200):
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
            status = save_project(url_project)

            logger.write(str(project_id) + "," + str(page_id) + "," + str(status) + "," + url_project + "\n")
            print(str(project_id) + "," + str(page_id) + "," + str(status) + "," + url_project)
            project_id = project_id + 1
            time.sleep(1)


def seek_categories(host="https://www.kickstarter.com/discover/"):
    category_list = []
    response = requests.get(host)
    soup = BeautifulSoup(response.text, "html.parser")
    body = soup.find("body")
    main_content = body.find("main")

    categories = main_content.findAll("ul", "columns2-sm w50-sm")
    for cat in categories:
        subcategories = cat.findAll("li", "js-subcategory block")
        for subcat in subcategories:
            data = subcat["data-category"]
            category_list.append(int(json.loads(data)["id"]))

    for category_id in category_list:
        response = requests.get(host + "advanced?category_id=" + str(category_id) + "&page=1")
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.find("title").text
        if title == "The page you were looking for doesn't exist (404)":
            pass
        elif len(title[12:][:-15].split(" / ")) == 1:
            pass
        else:
            with open("logs/category_" + str(category_id) + ".csv", "w") as logger:
                seek_projects(host + "advanced?category_id=" + str(category_id), logger)
                # break


if __name__ == "__main__":
    seek_categories()
