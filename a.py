import tweepy
import urllib
import time
from PIL import Image
import os
import MySQLdb
import threading
import time
#get auth.......
def get_auth():
    consumer_key='1L0RUDDJksJMViQ4GmBTFFxOn'
    consumer_secret='E9x8RJXkfsc9z6Z5wGNUEUvA8a2IVsYtAudTmfHEhr5ZI0RX3V'
    access_token='885743879114285056-aqMU2cp9kvoZ9fNNa0fOOp5sSxi6HSv'
    access_token_secret='lJMHFJVgOMJChFlsao9t21LGe87HEII3jrlIsIMgjt33c'
    auth=tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api=tweepy.API(auth)
    return api
#

#configuration

dict={'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
dir='../myblog/static/img/twitter/'
Twittercount = 20
looptime=10

#dir='data/'+str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))+usr
def tranTimetoNum(c):
    return c[0:4]+c[5:7]+c[8:10]+c[11:13]+c[14:16]+c[17:19]

def record(id,usr):
    args=(id,)
    cur.execute('select max(pub_date) from apps_twitter where twittername_id=%s',args)
    v=cur.fetchone()[0]
    if v!=None:
        max_time=str(v)
        max_time=int(tranTimetoNum(max_time))
    else:
        max_time=0
    for status in tweepy.Cursor(api.user_timeline, screen_name=usr).items(Twittercount):
        text=str(status._json['text'].encode('utf-8'))
        time=str(status._json['created_at'])
        month=dict[time[4:7]]
        pub_date = time[-4:]+'-'+month+'-'+time[8:10]+' '+time[11:19]+'.000000'
        pub_time=int(tranTimetoNum(pub_date))
        if pub_time<=max_time:
            break
        args=(text,pub_date,id)
        cur.execute('insert into apps_twitter (text,pub_date,twittername_id) values(%s,%s,%s)',args)
        cur.execute('select @@IDENTITY')
        twitter_id=str(cur.fetchone()[0])
        if 'media' in status.entities:
            i=0
            for image in status.entities['media']:
                f=urllib.urlopen(image['media_url'])
                imgdir=twitter_id+'-'+str(i)+'.jpg'
                with open (imgdir,'w+') as img:
                    img.write(f.read())
                imgdir='static/apps/img/twitter/'+twitter_id+'-'+str(i)+'.jpg'
                args=(imgdir,twitter_id)
                cur.execute('insert into apps_twitterimg (img, twitter_id) values (%s,%s)',args)
                i=i+1

# get text......
api=get_auth()
def milk():
    cur.execute('select id,name from apps_twitterlist')
    result=cur.fetchall()
    for i in result:
        record(str(i[0]),i[1])
    conn.commit()
    print 'Gotit'
#global timer
#timer=threading.Timer(looptime,milk)
#timer.start()

try:
    conn=MySQLdb.connect(host='localhost',user='root',passwd='Msqlmima',db='myblog',port=3306)
    cur=conn.cursor()
    #timer=threading.Timer(looptime,milk)
    #timer.start()
    #time.sleep(10)
    #timer.cancel()
    milk()
    cur.close()
    conn.close()
except MySQLdb.Error,e:
    print 'Mysql Error %d: %s' % (e.args[0], e.args[1])

