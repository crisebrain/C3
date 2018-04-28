from SearchEngine import cognitive_req
from Utils import SessionContainer
from InfoManager import InfoManager
from ConversationEngine import ChatBotWrapper

sc = SessionContainer()
jdata = sc.WhosNextEntry()
print(jdata["msgAns"])
chbw = ChatBotWrapper("4123434")
if True:
   jdata_new = chbw.interceptIntent()
else:
   jdata_new = cognitive_req(jdata)
sc.feedNextEntry(jdata_new)
sc.ShowSessionTree()
