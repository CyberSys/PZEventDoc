from generators.BaseGenerator import BaseGenerator
from PZEDGlobals import WantDeprecated

def getFileContents(path: str):
    file = open(path, 'r')
    return file.read()

class LuaCATSGenerator(BaseGenerator, extensions=["lua"]):
    # List of table names that have already been initialised
    initialisedTables: list[str]
    # The current level of indentation
    currentIndentation: int

    def __init__(self, wantDeprecated: WantDeprecated):
        """
        Class responsible for generating LuaCATS annotations

        :param wantDeprecated: Defines how deprecated objects should be treated
        """
        BaseGenerator.__init__(self, wantDeprecated)
        self.initialisedTables = []
        self.currentIndentation = 0
        try:
            self.totalString = getFileContents("extra.lua")
        except OSError:
            print("Could not read extra.lua")

    def writeLine(self, text: str):
        """
        Writes a line with the current level of indentation

        :param text: The text to write
        :return:
        """
        self.totalString += "    " * self.currentIndentation + f"{text}\n"

    def beginFile(self):
        """
        Adds the opening metadata to the file

        :return:
        """
        self.totalString = fileOpener

    @staticmethod
    def getFunctionSignature(data: dict) -> str:
        """
        Returns a function signature type description

        :param data: Rosetta callback definition
        :return:
        """
        signature = "fun("

        params = data.get("parameters")
        returns = data.get("returns")
        if params and len(params) != 0:
            doComma = False
            for parameter in params:
                if doComma:
                    signature += ","
                else:
                    doComma = True

                signature += f"{parameter['name']}:{parameter['type']}"
        elif not returns:  # callback has no parameters or return type
            return "function"
        signature += ")"

        if returns:
            signature += ":"
            name: str = returns.get("name")
            if name:
                signature += f"{name}:"
            signature += returns["type"]

        return signature

    @staticmethod
    def getCallbackDescription(callback: dict) -> str:
        description = ""

        notes: str = callback.get("notes")
        if notes:
            description = notes + "<br><br>"

        params: list[dict] = callback.get("parameters")
        if params:
            for param in params:
                notes: str = param.get("notes")
                if not notes:
                    continue
                description = description + f"{param['name']} - {notes}<br>"

        returnValue: dict = callback.get("returns")
        if returnValue:
            name = returnValue.get("name")
            if name:
                description = description + f"<br>Returns: {name}"
                notes: str = returnValue.get("notes")
                if notes:
                    description = description + f" - {notes}"

        return description

    @staticmethod
    def formatFunction(name: str, args: list[str]) -> str:
        """
        Returns an empty function declaration

        :param name: Name of the function to declare
        :param args: List of parameter names
        :return:
        """
        formattedArgs = ""
        if not (len(args) == 0):
            formattedArgs = args[0]
            for label in args[1:]:
                formattedArgs += f", {label}"

        return f"{name} = function({formattedArgs}) end,"

    def documentFunction(self, name: str, callbackType: str):
        """
        Documents a function that takes a single callback argument

        :param name: Name of the function
        :param callbackType: Name of the callback type
        :return:
        """
        self.writeLine("---@param callback " + callbackType)

        self.writeLine(self.formatFunction(name, ["callback"]))

    def documentType(self, name: str, data: dict):
        """
        Documents a function type

        :param name: Name of the type
        :param data: Rosetta formatted list of parameters
        :return:
        """
        self.writeLine("---" + self.getCallbackDescription(data))
        self.writeLine(f"---@alias {name} {self.getFunctionSignature(data)}\n")

    def initTable(self, name: str):
        """
        Initialises an empty lua table

        :param name: Name of the table
        :return:
        """
        self.writeLine(name + " = {}\n")
        self.initialisedTables.append(name)

    def document(self, name: str, data: dict, tableName: str = "Events"):
        """
        Documents an event/hook's callback type and Add/Remove functions

        :param name: Name of the event/hook
        :param data: Rosetta formatted event/hook data
        :param tableName: Name of the table containing the object (Events/Hook)
        :return:
        """
        deprecated: bool = data.get("deprecated", False)
        if not self.checkAllowDeprecated(deprecated):
            return

        if tableName not in self.initialisedTables:
            self.initTable(tableName)

        callbackType = "Callback_" + name
        self.documentType(callbackType, data['callback'])

        if deprecated:
            self.writeLine("---@deprecated")

        self.writeLine("---" + self.createDescription(
            data.get("name", name), data.get("notes", ""), deprecated, data.get("context", {}))
                       + "<br><br>" + self.getCallbackDescription(data['callback']))

        self.writeLine(f"{tableName}.{name} = {{")
        self.currentIndentation += 1

        self.documentFunction("Add", callbackType)
        self.documentFunction("Remove", callbackType)

        self.currentIndentation -= 1
        self.writeLine("}\n")

    def documentHook(self, name: str, data: dict):
        """
        Writes documentation for a hook

        :param name: Name of the hook
        :param data: Rosetta formatted hook data
        :return:
        """
        self.document(name, data, "Hook")

    def documentEvent(self, name: str, data: dict):
        """
        Writes documentation for an event

        :param name: Name of the event
        :param data: Rosetta formatted event data
        :return:
        """
        self.document(name, data, "Events")

    def documentCallback(self, name: str, data: dict):
        """
        Writes documentation for a callback

        :param name: Name of the callback
        :param data: Rosetta callback object
        :return:
        """
        self.documentType(name, data)
