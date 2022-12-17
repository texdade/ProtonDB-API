from flask import Flask, request
from requests_html import HTMLSession

import threading
import time
import json

app = Flask(__name__)

# FOR RETURN VALUE OF THREAD, PASS A LIST
# AND THREAD WILL PUT ITS RETURN VALUE TO
# THE LIST POSITION = TO ITS ID

class scraperThread(threading.Thread):
    def __init__(self, threadID, steamID):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.steamID = steamID
        self.gameBadge = None

    def run(self):
        print("Starting thread " + self.name + " with search id = " + self.steamID)

        session = HTMLSession()
        r = session.get('https://www.protondb.com/app/' + self.steamID)
        r.html.render()

        #beautifulsoup wrapper for 
        self.gameBadge = r.html.find("span", class_="MedalSummary__ExpandingSpan-sc-1fjwtnh-1 gjnWNf").text

        
#/badge?ids=1,2,3,4
@app.get('/badge')
def getBadges():
    idList = request.args.get('ids').split(",")
    threads = []
    badges = {}

    for i, steamID in enumerate(idList):
        thread = scraperThread(i, steamID)
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()
        print("Joined thread " + str(t.threadID))
        badges[t.steamID] = t.gameBadge

    return json.dumps(badges)

if __name__ == '__main__':
    app.run(debug=True)