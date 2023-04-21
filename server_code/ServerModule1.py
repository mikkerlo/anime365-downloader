import anvil.server
import anvil.http as http
import urllib.parse

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#
@anvil.server.callable
def get_anime_request(url):
  return http.request(url, headers={"User-Agent": "mikkerloAnimeDownload"}, json=True)

@anvil.server.callable
def get_direct_link(tr_id, name, access_token):
  resp = http.request(f"http://smotret-anime.com/api/translations/embed/{tr_id}?access_token={access_token}", json=True)
  data = resp['data']['stream']
  data_1080 = [i for i in data if i['height'] == 1080]
  if len(data_1080) == 0:
    return ""
  video_1080 = data_1080[0]['urls'][0]
  arg = urllib.parse.urlencode({'title': name})
  return video_1080 + '&' + arg
