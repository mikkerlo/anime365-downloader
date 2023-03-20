from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.http as http
import json

class TrInfo():
  def __init__(self, tr_id: int, authorsSummary: str):
    self.tr_id = tr_id
    self.authorsSummary = authorsSummary

  @staticmethod
  def from_tr_data(tr_data) -> 'TrInfo':
    return TrInfo(tr_data['id'], tr_data['authorsSummary'])

class EpInfo():
  def __init__(self, episodeInt: int, episodeFull: str, tranlations: list[TrInfo]):
    self.episodeInt = episodeInt
    self.episodeFull = episodeFull
    self.translations = tranlations

  @staticmethod
  def from_ep_data(ep_data) -> 'EpInfo':
    return EpInfo(ep_data['episodeInt'], ep_data['episodeFull'], [])

class AnimeInfo():
  anime_name: str
  last_ep: int
  def __init__(self, anime_name: str, last_ep: int, anime_id: int, episodes: list[EpInfo]):
    self.anime_name = anime_name
    self.last_ep = last_ep
    self.anime_id = anime_id
    self.episodes = episodes

  @staticmethod
  def from_anime_data(anime_data) -> 'AnimeInfo':
    return AnimeInfo(anime_data['titleLines'][0], anime_data['numberOfEpisodes'], anime_data['id'], [])

class Form1(Form1Template):
  ANIME_TYPES = [
      ('Russian subtitles', 'subRu'),
      ('English sybtitles', 'subEn'),
      ('RAW', 'raw'),
      ('Russian voice', 'voiceRu'),
      ('English voice', 'voiceEn'),
  ]
  
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.tr_type.items = self.ANIME_TYPES
    self.anime_info = None
    self.update_later()

  def update_later(self):
    if self.anime_info is None:
      self.label_tr.visible = False
      self.tr_author.visible = False
      self.counter.visible = False
      return

    self.label_tr.visible = True
    self.tr_author.visible = True
    self.counter.visible = True

  @staticmethod
  def make_query(url):
    return anvil.server.call('get_anime_request', url)

  def get_popularity(self, author_name) -> int:
    if self.anime_info is None:
      return 0
    episodes = self.anime_info.episodes
    cnt = 0
    for ep in episodes:
      authors = [i.authorsSummary for i in ep.translations]
      if author_name in authors:
        cnt += 1
    return cnt
  
  def load_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.load_button.enabled = False
    anime_id = int(self.anime_id.text)
    tr_type = self.tr_type.selected_value
    print(anime_id)
    self.anime_info = self.get_anime_ep_info(anime_id, tr_type)
    self.load_button.enabled = True
    episodes = self.anime_info.episodes
    translations = [item for i in episodes for item in i.translations]
    tr_authors = list(set([i.authorsSummary for i in translations]))
    tr_authors.sort(key=lambda x: -self.get_popularity(x))
    ep_count = min(self.anime_info.last_ep, len(episodes))
    self.anime_info.last_ep = ep_count
    self.tr_author.items = [('', None)] + [(i, i) for i in tr_authors]
    self.ep_ui.items = [{"epInfo": ep} for ep in self.anime_info.episodes]
    self.update_later()
    pass

  def update_on_default_tr(self, **event_args):
    if self.anime_info is None:
      return
    self.counter.text = f"{self.get_popularity(self.tr_author.selected_value)}/{self.anime_info.last_ep}"

    for ep_ui in self.ep_ui.get_components():
      ep_info = ep_ui.ep_info
      tr_id = None
      for tr in ep_info.translations:
        if tr.authorsSummary == self.tr_author.selected_value:
          tr_id = tr.tr_id
      if tr_id is not None:
        ep_ui.tr_author_1.selected_value = tr_id
        ep_ui.update_dropdown()

  @staticmethod
  def get_anime_data(anime_id) -> AnimeInfo:
    data = Form1.make_query(f"https://smotret-anime.ru/api/series/{anime_id}")
    ep_data = data['data']
    return ep_data

  @staticmethod
  def get_anime_ep_info(anime_id, tr_type):
    anime_data = Form1.get_anime_data(anime_id)
    anime_info = AnimeInfo.from_anime_data(anime_data)
    #return
    for ep in anime_data['episodes']:
      ep_info = EpInfo.from_ep_data(ep)
      print(ep)
      tr_data = Form1.make_query(f"http://smotret-anime.ru/api/episodes/{ep['id']}")
      for tr in tr_data['data']['translations']:
        if tr['type'] not in [i[1] for i in Form1.ANIME_TYPES]:
          print(tr['type'])
          continue
        if tr['type'] != tr_type:
          continue
        if tr['height'] != 1080:
          continue
        print(tr)
        tr_info = TrInfo.from_tr_data(tr)
        ep_info.translations.append(tr_info)
      anime_info.episodes.append(ep_info)
    return anime_info


    

