from generators.BaseGenerator import BaseGenerator


class MarkdownGenerator(BaseGenerator):
    def __init__(self, wantDeprecated):
        BaseGenerator.__init__(self, wantDeprecated)
        self.initialisedTables = []

    def getParameterString(self, parameters: list[dict] | dict = {}) -> str:
        result = ""
        if isinstance(parameters, list):
            for i in range(len(parameters)):
                result += "{}: {}<br>".format(i + 1, self.getParameterString(parameters[i]))
            return result

        for param in parameters:
            result += "{} {}, ".format(parameters[param], param)
        return result

    def initTable(self, name: str):
        self.writeLine("# " + name)
        self.writeLine("Name | Description | Parameters")
        self.writeLine("--- | --- | ---")
        self.initialisedTables.append(name)

    def document(self, name: str, data: dict, tableType="Events"):
        deprecated: bool = data.get("deprecated", False)
        if not self.checkAllowDeprecated(deprecated):
            return

        if tableType not in self.initialisedTables:
            self.initTable(tableType)

        self.writeLine("{} | {} | {}".format(
            name,
            self.getDescription(data.get("description", ""), deprecated, data.get("context", {})),
            self.getParameterString(data.get("parameters", []))
        ))

    def documentHook(self, name: str, data: dict):
        self.document(name, data, "Hook")

    def documentEvent(self, name: str, data: dict):
        self.document(name, data, "Events")
