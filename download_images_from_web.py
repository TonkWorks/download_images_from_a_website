#!/usr/bin/env python

import traceback
import argparse
import os
import shutil
import re


#Function Info goes here.
__info__ = {
	'title': "Download all images from a web page",
    'description': "Downloadall images from a web page",
    'url': "https://github.com/TonkWorks/pepper-autocomplete-atom-package", 
	'author': "Kevin Dagostino",
    'input': [
        {
            'label': 'Web Page URL to download pictures from',
            'type': 'text',
            'map': 'site_url',
        }
    ]
}



#And the actual script.
def script():
    import requests
    from bs4 import BeautifulSoup
    parser=argparse.ArgumentParser()
    parser.add_argument('--site_url')

    args=parser.parse_args()
    site_url = args.site_url

    r = requests.get(site_url)
    soup = BeautifulSoup(r.text)

    #images = [a['src'] for a in soup.find_all("img", {"src": re.compile("gstatic.com")})]

    images = soup.findAll("img")
    print("Found " + str(len(images)) + " images.")
    for image in images:
        try:
            #Make a filename for the image.
            filename = image["src"].split("/")[-1]
            filename ="".join([c for c in filename if c.isalpha() or c.isdigit() or c==' ' or c=='.']).rstrip() #Only valid OS chars
            filename = os.path.join(os.getcwd(), filename)


            #Fix relative images
            if (not image["src"].lower().startswith("http") and not image["src"].lower().startswith("data") ):
                #Relative image add full path
                print(image["src"])
                image["src"] = site_url + image["src"]
            print(image["src"])

            response = requests.get(image["src"])
            if response.status_code == 200:
                f = open(filename, 'wb')
                f.write(response.content)
                f.close()
                #print (filename)
        except Exception as e:
            traceback.print_exc()
            print(str(e))

if __name__ == '__main__':
	script()
