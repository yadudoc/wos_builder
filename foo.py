import json
import textstat

pubs = json.load(open("publications.json"), 'r')

for pub in pubs["publications"]:
    print pub['wos_id']
