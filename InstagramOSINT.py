

frombs4importBeautifulSoup
importjson
importos
importrequests
importrandom
importstring
importsys
importtime


classcolors:
HEADER='\033[95m'
OKBLUE='\033[94m'
OKGREEN='\033[92m'
WARNING='\033[93m'
FAIL='\033[91m'
ENDC='\033[0m'
BOLD='\033[1m'
UNDERLINE='\033[4m'


classInstagramOSINT:

def__init__(self,username):
 self.username=username
self.useragents=['Mozilla/5.0(WindowsNT6.1;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/54.0.2840.99Safari/537.36',
'Mozilla/5.0(WindowsNT10.0;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/54.0.2840.99Safari/537.36',
'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/54.0.2840.99Safari/537.36',
'Mozilla/5.0(Macintosh;IntelMacOSX10_12_1)AppleWebKit/602.2.14(KHTML,likeGecko)Version/10.0.1Safari/602.2.14',
'Mozilla/5.0(WindowsNT10.0;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/54.0.2840.71Safari/537.36',
'Mozilla/5.0(Macintosh;IntelMacOSX10_12_1)AppleWebKit/537.36(KHTML,likeGecko)Chrome/54.0.2840.98Safari/537.36',
'Mozilla/5.0(Macintosh;IntelMacOSX10_11_6)AppleWebKit/537.36(KHTML,likeGecko)Chrome/54.0.2840.98Safari/537.36',
'Mozilla/5.0(WindowsNT6.1;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/54.0.2840.71Safari/537.36',
'Mozilla/5.0(WindowsNT6.1;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/54.0.2840.99Safari/537.36',
'Mozilla/5.0(WindowsNT10.0;WOW64;rv:50.0)Gecko/20100101Firefox/50.0']

self.scrape_profile()


def__repr__(self):
returnf"CurrentUsername:{self.username}"

def__str__(self):
returnf"CurrentUsername:{self.username}"

def__getitem__(self,i):
returnself.profile_data[i]


defscrape_profile(self):
"""
Thisisthemainscrapewhichtakestheprofiledataretrievedandsavesitintoprofile_data
:params:None
:return:profiledata
"""
#Getthehtmldatawiththerequestsmodule
r=requests.get(f'http://instagram.com/{self.username}',headers={'User-Agent':random.choice(self.useragents)})
soup=BeautifulSoup(r.text,'html.parser')
#Findthetagsthatholdthedatawewanttoparse
general_data=soup.find_all('meta',attrs={'property':'og:description'})
more_data=soup.find_all('script',attrs={'type':'text/javascript'})
description=soup.find('script',attrs={'type':'application/ld+json'})
#Trytoparsethecontent--ifitfailsthentheprogramexits
try:
text=general_data[0].get('content').split()
self.description=json.loads(description.get_text())
self.profile_meta=json.loads(more_data[3].get_text()[21:].strip(';'))

except:
print(colors.FAIL+f"Username{username}notfound"+colors.ENDC)
return1
self.profile_data={"Username":self.profile_meta['entry_data']['ProfilePage'][0]['graphql']['user']['username'],
"Profilename":self.description['name'],
"URL":self.description['mainEntityofPage']['@id'],
"Followers":text[0],"Following":text[2],"Posts":text[4],
"Bio":str(
self.profile_meta['entry_data']['ProfilePage'][0]['graphql']['user']['biography']),
"profile_pic_url":str(self.profile_meta['entry_data']['ProfilePage'][0]['graphql']['user'][
'profile_pic_url_hd']),
"is_business_account":str(
self.profile_meta['entry_data']['ProfilePage'][0]['graphql']['user'][
'is_business_account']),
"connected_to_fb":str(self.profile_meta['entry_data']['ProfilePage'][0]['graphql']['user'][
'connected_fb_page']),
"externalurl":str(
self.profile_meta['entry_data']['ProfilePage'][0]['graphql']['user']['external_url']),
"joined_recently":str(self.profile_meta['entry_data']['ProfilePage'][0]['graphql']['user'][
'is_joined_recently']),
"business_category_name":str(
self.profile_meta['entry_data']['ProfilePage'][0]['graphql']['user'][
'business_category_name']),
"is_private":str(
self.profile_meta['entry_data']['ProfilePage'][0]['graphql']['user']['is_private']),
"is_verified":str(
self.profile_meta['entry_data']['ProfilePage'][0]['graphql']['user']['is_verified'])}

returnself.profile_data


defscrape_posts(self):
"""Scrapesallpostsanddownloadsthem
:return:none
:param:none
"""
ifself.profile_data['is_private'].lower()=='true':
print("[*]Privateprofile,cannotscrapephotos!")
return1
else:
posts={}
forindex,postinenumerate(self.profile_meta['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']):
os.mkdir(str(index))
posts[index]={"Caption":str(post['node']['edge_media_to_caption']['edges'][0]['node']['text']),
"NumberofComments":str(post['node']['edge_media_to_comment']['count']),
"CommentsDisabled":str(post['node']['comments_disabled']),
"TakenAtTimestamp":str(post['node']['taken_at_timestamp']),
"NumberofLikes":str(post['node']['edge_liked_by']['count']),
"Location":str(post['node']['location']),
"AccessabilityCaption":str(post['node']['accessibility_caption'])
}

#Downloadsthethumbnailsofthepost
#Pictureisjustanintindexoftheurlinthelist
withopen(f'{os.getcwd()}/{index}/'+''.join([random.choice(string.ascii_uppercase)forxinrange(random.randint(1,9))])+'.jpg','wb')asf:
#Delaytherequesttimesrandomly(benicetoInstagram)
time.sleep(random.randint(5,10))
r=requests.get(post['node']['thumbnail_resources'][0]['src'],headers={'User-Agent':random.choice(self.useragents)})
#Takesthecontentofrandputsitintothefile
f.write(r.content)

withopen('posts.txt','w')asf:
f.write(json.dumps(posts))

defmake_directory(self):
"""Makestheprofiledirectoryandchangesthecwdtoit
thisshouldonlybecalledfromthesave_datafunction!
:return:True
"""
try:
os.mkdir(self.username)
os.chdir(self.username)
exceptFileExistsError:
num=0
whileos.path.exists(self.username):
num+=1
try:
os.mkdir(self.username+str(num))
os.chdir(self.username+str(num))
exceptFileExistsError:
pass

defsave_data(self):
"""Savesthedatatotheusernamedirectory
:return:none
:param:none
"""
self.make_directory()
withopen('data.txt','w')asf:
f.write(json.dumps(self.profile_data))
#DownloadstheprofilePicture
self.download_profile_picture()
print(f"Saveddatatodirectory{os.getcwd()}")

defprint_profile_data(self):
"""Printsoutthedatatothescreenbyiteratingthroughthedictwithit'skeyandvalue
:return:none
:param:none
"""
#Printthedataouttotheuser
print(colors.HEADER+"---------------------------------------------"+colors.ENDC)
print(colors.OKGREEN+f"Results:scanfor{self.profile_data['Username']}oninstagram"+colors.ENDC)
forkey,valueinself.profile_data.items():
print(key+':'+value)

defdownload_profile_picture(self):
"""Downloadstheprofilepicandsavesittothedirectory
:return:none
:param:none
"""
withopen("profile_pic.jpg","wb")asf:
time.sleep(1)
r=requests.get(self.profile_data['profile_pic_url'],headers={'User-Agent':random.choice(self.useragents)})
f.write(r.content)

