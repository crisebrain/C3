from SearchEngine import cognitive_req
from Utils import SessionContainer
from InfoManager import InfoManager
from ConversationEngine import ChatBotWrapper

im = InfoManager(SessionContainer, ChatBotWrapper, cognitive_req)
jdata = im.newconsult()
im.newAnswer(jdata)
jdata = im.newconsult()
im.newAnswer(jdata)
jdata = im.newconsult()
im.newAnswer(jdata)
# sc = SessionContainer()
# jdata = sc.WhosNextEntry()
# print(jdata["msgAns"])
# chbw = ChatBotWrapper(jdata["IdChatBot"])
# if True:
#    jdata_new = chbw.interceptIntent()
# else:
#    jdata_new = cognitive_req(jdata)
# sc.feedNextEntry(jdata_new)
# sc.ShowSessionTree()
