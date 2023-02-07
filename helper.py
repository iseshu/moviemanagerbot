from doodstream import DoodStream
import cloudinary ,httpx,requests
import json
import replicate
import cloudinary.uploader
import time
import cloudscraper
from bs4 import BeautifulSoup


cloudinary.config(
    cloud_name = 'yss-projects',
    api_key = '663483921387345',
    api_secret = '3tWGt10OeDzWfaQ-V4CIO3Wv8tU'
)
las_data = "https://ibomma-data.yss.workers.dev/lastdatamoviesgroup"
all_data = "https://ibomma-data.yss.workers.dev/allgroupdata"
data_url = 'https://ibomma-data.yss.workers.dev/'
url = "https://movierulz.vercel.app/"
content_url = "https://movierulz.vercel.app/get?url={}"

def img_quality(url):
  model = replicate.models.get("tencentarc/gfpgan")
  version = model.versions.get("9283608cc6b7be6b65a8e44983db012355fde4132009bf99d976b2f0896856a3")
  inputs = {
    'img': url,
    'version': "v1.4",
    'scale': 11,
  }
  output = version.predict(**inputs)
  return output
def gen_mdisk(link):
  url = 'https://diskuploader.mypowerdisk.com/v1/tp/cp'
  param = {
      'token':'TAZn97Y53EAYGcFFpyih',
      'link':link
      }
  res = httpx.post(url, json = param).json()['sharelink']
  return res

def dood_upload(link):
  d = DoodStream("57266yi9vs1ox1e18c28g")
  upload = d.remote_upload(link)
  return upload['result']['embed_url']

def image_uploader(link):
  uploa = cloudinary.uploader.upload(link)
  return uploa['secure_url']

def update_data(title,description,url,image):
  data = httpx.get(all_data).json['data']
  dat = {"title":title,"link":url,"description":description,'image':image}
  data.append(dat)
  req = requests.post(data_url,json.dumps({"data":data,"_id":"allgroupdata"}))

def shorten_link(link):
  url = " https://api.shareus.in/shortLink?token=mwNmsweDmVeJozfD5BWvISamwYk2&format=json&link={}".format(link)
  return httpx.get(url).json()['shortlink']

def ome_mdisk(url):
  client = cloudscraper.create_scraper(allow_brotli=False)
  DOMAIN = "https://mdisk.pro"
  ref = "https://m.meclipstudy.in/"
  h = {"referer": ref}
  resp = client.get(url, headers=h)
  soup = BeautifulSoup(resp.content, "html.parser")
  inputs = soup.find_all("input")
  data = {input.get('name'): input.get('value') for input in inputs}
  h = {"x-requested-with": "XMLHttpRequest"}
  time.sleep(8)
  r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
  try:
      return r.json()['url']
  except:
      return "Something went wrong :("
