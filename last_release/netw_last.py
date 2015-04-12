import re
import oauth2
import time
import urllib2
import json
import datetime
url1 = "https://api.twitter.com/1.1/search/tweets.json"
params = {
"oauth_version": "1.0",
"oauth_nonce": oauth2.generate_nonce(),
"oauth_timestamp": int(time.time())
}
consumer = oauth2.Consumer(key="cjHyScOjbZovExUpVplBeW8N3", secret="Ipvjnv1Vqxbm8lCcNNvugVNFpxBZUYjRLuuyQh8nfBN59uvIQp")    # access to twitter (Guys, read aboaut oauth authintification)
token = oauth2.Token(key="1321179289-yxxikf1x7uRPh0sQLCuL5z2JtKDArZYH7gCFBuy", secret="e7wIue8Kg2WWcmq0IPIvLikTARAJwuSt3NN7Mf2EWOL7J")
params["oauth_consumer_key"] = consumer.key
params["oauth_token"] = token.key
prev_id=int(433057813859155968)
users_dict={"Nikolay":("#Arsenal","en"),"Javier1":("#Barcelona","es"),"Helene":("#PSG","es"),"Ribale":("#Marseille","fr")}
search_str=""
#searching_date=datetime.datetime.today()
#print searching_date.isoformat()[:10]
for tupl in users_dict.values():
    search_str=search_str+str(tupl[0])+" OR "
search_str=search_str[0:-4]
for i in range(4):      #change number in scope to get more results(it should be forever loop but this just for testing)
    print ("-------------------------------------------------------NEW-------------------------------------") # debugging stuff
    url=url1
    params["q"]=search_str
    params["count"]=90          #number of tweets to download (not more than 180 every 15 min(tweeter api restriction))
    params["geocode"] = ""
    params["lang"] = ""
    params["locale"] = ""
    params["result_type"] = "" 
    params["until"] ="" 
    params["since_id"] = str(prev_id) # specify start point of searching
    params["max_id"] = ""
    req = oauth2.Request(method="GET", url=url, parameters=params)
    signature_method = oauth2.SignatureMethod_HMAC_SHA1()
    req.sign_request(signature_method, consumer, token)
    headers = req.to_header()
    url = req.to_url()
    response=urllib2.Request(url)
    data = json.load(urllib2.urlopen(response))
    #print data;
    #print data["statuses"][1].get("text") 
    if data["statuses"] == []:
        print "end of data" 
        continue
    else:
        prev_id = data["statuses"][-1]["id_str"] # create a candididate for the latest tweet
        #print prev_id, i
    #f = open("outfile_" + str(i) + ".txt", "w") #file with all data
    #json.dump(data["statuses"], f)
    for tweet in data["statuses"]:
        filenames=[key for key,value in users_dict.items() if ((value[1]==tweet["lang"]) and (value[0] in tweet["text"]) and (tweet["retweet_count"]==0)) ]
        for name in filenames:
            f_app=open(name+".txt","a")
            json.dump(tweet["text"],f_app)
            f_app.write("\n")
            f_app.close()
       # if tweet["retweet_count"]==0:
        if (tweet["id_str"]>prev_id):
            prev_id=tweet["id_str"]  #(checking if our prev_id the biggest one)
        #print tweet["id_str"]
    #f.close()
    time.sleep(10)

