from ._anvil_designer import ItemTemplate1Template
from anvil import *
import anvil.server

class ItemTemplate1(ItemTemplate1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.ep_info = self.item['epInfo']
    self.episodeName.text = self.ep_info.episodeFull
    self.tr_author_1.items = [(i.authorsSummary, i.tr_id) for i in self.ep_info.translations]
    self.update_dropdown()
    # Any code you write here will run before the form opens.

  def update_dropdown(self, **lmao):
    self.download_ep.url = f"https://smotret-anime.com/translations/mp4/{self.tr_author_1.selected_value}?format=mp4&height=1080"
    self.download_ep.tr_id = self.tr_author_1.selected_value
    self.download_subtitles.url = f"https://smotret-anime.com/translations/ass/{self.tr_author_1.selected_value}?download=1"
    