import tweepy
import urllib
import time
import sys

reload(sys)
sys.setdefaultencoding('utf8')
#get auth.......
#configuration
Twittercount = 1
dict={'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
def tranTimetoNum(c):
    return c[0:4]+c[5:7]+c[8:10]+c[11:13]+c[14:16]+c[17:19]

#dir='data/'+str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))+usr

def record(usr):
    consumer_key='Ns07lqUcfNJLa7QVGAcPfDCmY'
    consumer_secret='p04unq4ppJ1kCQhmK5q4XFkh91dtSEez8CMW2lS76qpeVM0V7B'
    access_token='885743879114285056-txRs5gfBmdSDVDItkh9JpvhVg9a4yHD'
    access_token_secret='CP1hNH657dOb92xTEApXHFoj3bfBdRXgqWYNHgzxx0zX8'
    auth=tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api=tweepy.API(auth)
    i=0
    for status in tweepy.Cursor(api.user_timeline, screen_name=usr).items(Twittercount):
        text=str(status._json['text'].encode('utf-8'))
        time=str(status._json['created_at'])
        #print time
        month=dict[time[4:7]]
        pub_date = time[-4:]+'-'+month+'-'+time[8:10]+' '+time[11:19]+'.000000'
        pub_time=str(tranTimetoNum(pub_date))
        if 'media' in status.entities:
            i=0
            for image in status.entities['media']:
                f=urllib.urlopen(image['media_url'])
                with open (pub_time+str(i)+'.jpg','w+') as img:
                    img.write(f.read())
                i=i+1
    return text,pub_time,i
# get text......


#global timer
#timer=threading.Timer(looptime,milk)
#timer.start()
