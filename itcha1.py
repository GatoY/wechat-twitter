import itchat
from itchat.content import *

@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    itchat.send('%s: %s' % (msg['Type'], msg['Text']),toUserName='filehelper')

@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    msg['Text'](msg['FileName'])
    return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])

@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO],isGroupChat = True)
def download_files(msg):
    msg['Text'](msg['FileName'])
    itchat.send('@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName']),toUserName='filehelper')

@itchat.msg_register(TEXT, isGroupChat = True)
def groupchat_reply(msg):
    itchat.send(u'@%s\u2005I  %s' % (msg['ActualNickName'], msg['Content']), toUserName='filehelper')

itchat.auto_login(True)
itchat.run()
