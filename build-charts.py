#!/usr/bin/env python3

from glob import glob
from os import path
import yaml
import json
import shutil
from datetime import datetime
import markdown

catalogPath = "catalog.json"
sourceFolder = "src"
trainName = "charts"

def main():
    lastUpdate = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    catalog = {}
    catalog[trainName] = {}

    charts = glob(path.join(sourceFolder, "*"))
    for chartFolder in charts:        
        chartFilePath = path.join(chartFolder, "Chart.yaml")
        with open(chartFilePath) as openedFile:
            chartFile = yaml.safe_load(openedFile)

        appName = chartFile["name"]
        humanVersion = "{}_{}".format(chartFile["appVersion"], chartFile["version"])

        print("{}: {}".format(appName, humanVersion))

        readmeFilePath = path.join(chartFolder, "app-readme.md")
        with open(readmeFilePath) as openedFile:
            readmeContent = markdown.markdown(openedFile.read())

        itemFileSrcPath = path.join(chartFolder, "item.yaml")
        with open(itemFileSrcPath) as openedFile:
            itemInfo = yaml.safe_load(openedFile)

        destFolder = path.join(trainName, appName, chartFile["version"])
        shutil.copytree(chartFolder, destFolder, dirs_exist_ok=True)

        itemFileDestPath = path.join(trainName, appName, "item.yaml")
        shutil.copyfile(itemFileSrcPath, itemFileDestPath)
        
        catalog[trainName][appName] = {
            "app_readme": readmeContent,
            "categories": itemInfo["categories"],
            "description": chartFile["description"],
            "healthy": True,
            "healthy_error": None,
            "home": chartFile["home"],
            "location": "/__w/charts/" + appName,
            "latest_version": chartFile["version"],
            "latest_app_version": chartFile["appVersion"],
            "latest_human_version": humanVersion,
            "last_update": lastUpdate,
            "name": appName,
            "recommended": False,
            "title": chartFile["annotations"]["title"],
            "maintainers": chartFile["maintainers"],
            "tags": itemInfo["tags"],
            "screenshots": itemInfo["screenshots"],
            "sources": chartFile["sources"],
            "icon_url": itemInfo["icon_url"]
        }
    
    with open(catalogPath, mode="w") as catalogFile:
        json.dump(catalog, catalogFile, sort_keys=True, indent=4)

if __name__ == "__main__":
    main()