import googlemaps

API_KEY = "AIzaSyCHd8gLL4I7LfR8KtOEEv1TJF3Te0As7mU"


# MAIN
if __name__ == "__main__":

  # TESTS

  gmaps = googlemaps.Client(key=API_KEY)
  res = gmaps.places("Paris")
  print(res)
