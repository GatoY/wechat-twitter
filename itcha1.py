import itchat
import a
from itchat.content import *
import urllib
import sys
reload(sys)
sys.setdefaultencoding('utf8')
@itchat.msg_register(TEXT)
def text_reply(msg):
    usr=msg['Text'][
    #print usr
    text,pub_time,i=a.record(usr)
    #print text
    print type(text)
    #text=str(text)
    #itchat.send('I\'m OK to send to you!',toUserName='filehelper')
    itchat.send(text,toUserName='filehelper')
    for count in xrange(i):
        itchat.send_image(pub_time+str(count)+'.jpg',toUserName='filehelper')
#itchat.send_image('201710060216320.jpg',toUserName='filehelper')
itchat.auto_login(True)
itchat.run()
