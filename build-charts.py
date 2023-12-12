#!/usr/bin/env python3

from glob import glob
from os import path
import yaml
import json
import shutil
from datetime import datetime
import markdown

catalogPath = "catalog.json"
trainName = "charts"
sourceFolder = "./library/ix-dev/" + trainName

def main():
    lastUpdate = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    catalog = {}
    catalog[trainName] = {}

    charts = glob(path.join(sourceFolder, "*"))
    for chartFolder in charts:        
        chartFilePath = path.join(chartFolder, "Chart.yaml")
        with open(chartFilePath) as openedFile:
            chartFile = yaml.safe_load(openedFile)
        
        questionsFilePath = path.join(chartFolder, "questions.yaml")
        with open(questionsFilePath) as openedFile:
            questionsFile = yaml.safe_load(openedFile)

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

        appVersionsPath = path.join(trainName, appName, "app_versions.json")
        with open(appVersionsPath) as openedFile:
            appVersions = json.load(openedFile)
        appVersions[chartFile["version"]] = {
            "healthy": True,
            "healthy_error": None,
            "supported": True,
            "location": "/__w/charts/" + appName,
            "last_update": lastUpdate,
            "required_features": [],
            "human_version": humanVersion,
            "version": chartFile["version"],
            "chart_metadata": {
                "kubeVersion": ">=1.24.0",
                "apiVersion": "v2",
                "name": appName,
                "version": chartFile["version"],
                "appVersion": chartFile["appVersion"],
                "description": chartFile["description"],
                "home": chartFile["home"],
                "icon": itemInfo["icon_url"],
                "deprecated": False,
                "sources": chartFile["sources"],
                "maintainers": chartFile["maintainers"],
                "keywords": chartFile["keywords"],
                "dependencies": chartFile["dependencies"],
                "annotations": {
                    # "max_scale_version": "23.10.1",
                    # "min_scale_version": "22.12.4",
                },
            },
            "app_metadata": None,
            "schema": questionsFile,
            "app_readme": readmeContent,
            "detailed_readme": readmeContent,
            "changelog": "",
        }
        with open(appVersionsPath, mode="w") as openedFile:
            json.dump(appVersions, openedFile, sort_keys=True, indent=4)
    
    with open(catalogPath, mode="w") as catalogFile:
        json.dump(catalog, catalogFile, sort_keys=True, indent=4)

if __name__ == "__main__":
    main()