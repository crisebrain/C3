from time import time
import re

class InfoManager:
    def __init__(self, SessionContainer, ChatBotWrapper):
        """Creates the Info Manager for the current conference session."""
        self.conference_date = time()
        self.conference = {}
        self.sc = SessionContainer(ChatBotWrapper)

    def newConsult(self):
        """Creates new conversation Flow with the IntentTree class.
        Outputs:
        Json with the info for the conversation nodes,
                 each node with the info about the id chatBot."""
        # jdata["msgAns"] = self.outputMsg(jdata["msgAns"])
        return self.sc.WhosNextEntry()

    def intentFlow(self, jdata, cbwrapper, se):
        """Extracts the value from the msgOriginal with the extractValue
        function, then is stored into node from msgReq and msgAns taken.
        If state is valid the msg is formated, saved to msgAnsd element into
        jdata dictionary and passed to cbwrapper.
        In other cases this searchs into the database or CSE for the intent.
        Parameters:
        jdata - Node information dictionary.
        cbwrapper - ChatBotWrapper instance object.
        se - Search Engine function.
        """
        if jdata["state"] == "valid":
            # Extraer valor ***********************************
            jdata = self.extractValue(jdata)
            # Extraer valor ***********************************
            self.sc.feedNextEntry(jdata)
            msgAns = self.outputMsg(jdata)
            if isinstance(msgAns, str):
                jdata["msgAnsd"] = msgAns
                cbwrapper.generateAnswer(jdata)
            else:
                print("Funcion para saltar hacia el nodo no lleno y reordenar")

            # self.sc.fill_node(jdata)
        elif jdata["state"] == "no_valid":
            print("ChatBotWrapper no solucionó")
            print("Buscando en bases de datos\n")
            print("Buscando con mecanismo cognitivo\n")
            jdata_ans = se(jdata)
            for intent in jdata_ans:
                self.sc.feedNextEntry(intent)
                cbwrapper.generateAnswer(intent)

    def extractValue(self, jdata):
        """Extracts the value from msgOriginal string from jdata dict."""
        msgOriginal = jdata["msgOriginal"]
        # ****************************************************
        # extraer valor, condiciones *************************
        value = msgOriginal.split(" ")[-1]
        # ****************************************************
        jdata.update({"value":value})
        return jdata

    def outputMsg(self, jdata):
        """formats the msgAns with the values from upper nodes."""
        msgString = jdata["msgAns"]
        namestr = jdata["name"]
        pattern = r"\$\w+"
        fields = re.findall(pattern=pattern, string=msgString)
        if isinstance(fields, list):
            for field in fields:
                fieldw = field[1:]
                tree = self.sc.extractTree()
                node = tree.findFieldContext(fieldw, namestr)
                if node is None:
                    raise ValueError("Key not stored at context %s"%fieldw)
                else:
                    if node.value is None:
                        print("No previosly filled node, jumping")
                        return node
                    else:
                        msgString = msgString.replace(field, node.value)
        return msgString
