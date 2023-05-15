"""
MIT License

Copyright (c) 2023 Albion

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# if it work helped you, please consider leaving me a tip ^u^
# https://ko-fi.com/starseamstress

import sys, json, getopt

schemaFile = "schema.json"
outputFile = "Events.lua"
currentIndentation = 0

allowDeprecated = False
onlyDeprecated = False

def loadOptions():
    global allowDeprecated, onlyDeprecated, schemaFile, outputFile
    opts, _ = getopt.getopt(sys.argv[1:],"dDs:o:")
    for option, argument in opts:
        if option == "-d":
            allowDeprecated = True
        elif option == "-D":
            onlyDeprecated = True
        elif option == "-i":
            schemaFile = argument
        elif option == "-o":
            outputFile = argument

def loadSchema():
    global schema
    file = open(schemaFile, "r", encoding="utf-8")
    schema = json.loads(file.read())
    file.close()

def toFile(str):
    file = open(outputFile, "w", encoding="utf-8")
    file.write(str)
    file.close()



def newLine():
    return "\n" + "    " * currentIndentation



def getFunctionSignature(params):
    if not isinstance(params, dict) or len(params) == 0:
        return "function"
    
    formattedParams = ""
    doComma = False
    for label in params:
        if doComma:
            formattedParams += ","
        else:
            doComma = True

        formattedParams += label + ":" + params[label]

    return "fun({}):any".format(formattedParams)

def writeFunction(name, args=None):
    formattedArgs = ""
    if not (args == None or len(args) == 0):
        formattedArgs = args[0]
        for label in args[1:]:
            formattedArgs += ", " + label

    return "{} = function({}) end,".format(name, formattedArgs)

def documentFunction(name, params=None):
    global totalString
    def writeFuncParam(params):
        global totalString
        totalString += newLine() + "---@param func " + getFunctionSignature(params)

    #EmmyLua doesn't seem to support overloads specifying function parameters, but maybe in the future
    if isinstance(params, list):
        writeFuncParam(params[0])
        for i in range(1, len(params)):
            totalString += newLine() + "---@overload fun(func:{})".format(getFunctionSignature(params[i]))
    else:
        writeFuncParam(params)

    totalString += newLine() + writeFunction(name, ["func"])



def getTableDescription(description="", deprecated=False, clientOnly=False, serverOnly=False):
    if clientOnly:
        description = "(Client Only) " + description
    elif serverOnly:
        description = "(Server Only) " + description
    if deprecated:
        description = "(Deprecated) " + description + newLine() + "---@deprecated"
    
    return description

def initTable(type):
    global totalString
    totalString += newLine() + type + " = {}\n"

def openTable(name, description=None):
    global totalString, currentIndentation
    if description != "":
        totalString += newLine() + "---" + description

    totalString += newLine() + name + " = {"
    currentIndentation += 1

def closeTable():
    global totalString, currentIndentation
    currentIndentation -= 1
    totalString += newLine() + "}"

def writeTable(event, data, tableName):
    deprecated = data.get("deprecated", False)
    if onlyDeprecated:
        if not deprecated: return
    elif deprecated and not allowDeprecated: return
    
    openTable(tableName + "." + event, getTableDescription(data.get("description", ""), deprecated, data.get("clientOnly", False), data.get("serverOnly", False)))

    documentFunction("Add", data.get("parameters"))
    documentFunction("Remove")

    closeTable()

loadOptions()
loadSchema()

totalString = """---@meta
-- Generated by PZEventDoc https://github.com/demiurgeQuantified/PZEventDoc

-- If it helped you, please consider leaving me a tip ^u^
-- https://ko-fi.com/starseamstress
"""

events = schema.get("Events")
if events:
    initTable("Events")
    for event in events:
        writeTable(event, events[event], "Events")
    totalString += newLine()

hooks = schema.get("Hook") or schema.get("Hooks")
if hooks:
    initTable("Hook")
    for hook in hooks:
        writeTable(hook, hooks[hook], "Hook")
    totalString += newLine()

toFile(totalString)