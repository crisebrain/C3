from ChatBotWrapper import ChatBotWrapper
chbfolder = "chatbots"
chb = ChatBotWrapper(chbfolder)
chb.current_intentTree
it = chb.current_intentTree
names = it.mandatoryChecker()
print(names)
