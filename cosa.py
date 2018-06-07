from ChatBotWrapper import ChatBotWrapper
chbw = ChatBotWrapper("chatfase1")
chbw = ChatBotWrapper("chatFase1")
chbw = ChatBotWrapper("chatbots")
chbw = ChatBotWrapper("chatbots", "chatfase1")
chbw.current_intentTree
from Utils import SessionContainer
SessionContainer?
sc = SessionContainer("Sessions/Conference.pck", "chatfase1")
it = sc.extractTree()
it
it.getOrderFromCurrent()
it.by_attr?
it.by_attr()
print(it.by_attr())
print(it.by_attr(attrname="contextIn"))
print(it.by_attr(attrname="contextin"))
print(it.by_attr(attrname="contextout"))
it.orderlist
it.setSession?
it.currentcontextls
it.childiter
it.childiter()
it.by_attr()
it.node.descendants
node.contextIn if len(getattr(node, "contextIn"))>0 for node in it.node.descendants
[node.contextIn if len(getattr(node, "contextIn"))>0 for node in it.node.descendants]
[node.contextIn for node in it.node.descendants if len(node.contextIn)>0]
%hist -f cosa.py
