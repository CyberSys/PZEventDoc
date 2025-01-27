# if my work helped you, please consider leaving me a tip ^u^
# https://ko-fi.com/starseamstress

import sys
import json
from getopt import getopt
from PZEDGlobals import *
import GeneratorManager
from generators import *


def loadOptions() -> tuple[str, str, WantDeprecated]:
    """
    Returns a tuple containing options passed at the command line

    :return: input filepath, output filepath, wantDeprecated
    """
    dataFile: str = "data.json"
    outputFile: str = "Events.lua"
    wantDeprecated: WantDeprecated = WantDeprecated.NONE

    opts, _ = getopt(sys.argv[1:], 'dDs:o:')
    for option, argument in opts:
        if option == '-d':
            wantDeprecated = WantDeprecated.ALLOW
        elif option == '-D':
            wantDeprecated = WantDeprecated.EXCLUSIVE
        elif option == '-s':
            dataFile = argument
        elif option == '-o':
            outputFile = argument

    return dataFile, outputFile, wantDeprecated


def readJson(path: str) -> dict:
    """
    Reads a Json file as a dictionary

    :param path: The path of the file to read
    :return: Dictionary representing the file contents
    """
    file = open(path, 'r', encoding='utf-8')

    fileDict: dict
    try:
        fileDict = json.loads(file.read())
    finally:
        file.close()

    return fileDict


if __name__ == "__main__":
    try:
        dataFile, outputFile, wantDeprecated = loadOptions()

        try:
            data = readJson(dataFile)
        except Exception as e:
            print("Error opening input file: " + str(e))
            raise e

        extension: str = outputFile.rsplit('.', 1)[1].lower()
        generator = GeneratorManager.getGenerator(extension, wantDeprecated)

        events: dict = data.get("events")
        if events:
            for name, event in events.items():
                generator.documentEvent(name, event)

        hooks: dict = data.get("hooks")
        if hooks:
            for name, hook in hooks.items():
                generator.documentHook(name, hook)

        callbacks: dict = data.get("callbacks")
        if callbacks:
            for name, callback in callbacks.items():
                generator.documentCallback(name, callback)

        try:
            generator.toFile(outputFile)
        except Exception as e:
            raise Exception("Error writing output file: " + str(e))
    except Exception as e:
        print("Annotation generation failed: " + str(e))