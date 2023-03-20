from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.http as http

class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  @staticmethod
  def make_query(url):
    return anvil.server.call(get_anime_request, url)
  
  def load_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.load_button.enabled = False
    anime_id = int(self.anime_id.text)
    print(anime_id)
    print(self.make_query(f"https://smotret-anime.ru/api/series/{anime_id}"))
    self.load_button.enabled = True
    pass


