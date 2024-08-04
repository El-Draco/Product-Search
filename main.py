import serpapi
import json
params = {
  "engine": "google",
  "google_domain":"google.ae",
  "q":"Green Fabric Sofa",
  "location":"Dubai,Dubai,United Arab Emirates",
  "gl":"ae",
  "cr":"countryAE",
  "api_key": "e7788240cff1f94267a8e201cf4857080e4a039fb499f4df1005f067a9e35c5b",
  "num":"1"
}

search = serpapi.search(params)
search = search.as_dict()
matches = search["shopping_results"]
print(json.dumps(matches, indent=4, sort_keys=True))