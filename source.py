#just something imports
from selenium.webdriver.firefox.options import Options
from fake_useragent import UserAgent
from stem.control import Controller
from subprocess import Popen, PIPE
#from selenium import webdriver
from seleniumwire import webdriver
from requests import get
from stem import Signal
import subprocess
import threading
import requests
import socket
import socks
import time
import sys
import os

#copyright
print('''
 ________                          ______   __  __                        __  
/        |                        /      \ /  |/  |                      /  |
$$$$$$$$/______    ______        /$$$$$$  |$$ |$$/   ______   _______   _$$ |_ 
   $$ | /      \  /      \       $$ |  $$/ $$ |/  | /      \ /       \ / $$   |
   $$ |/$$$$$$  |/$$$$$$  |      $$ |      $$ |$$ |/$$$$$$  |$$$$$$$  |$$$$$$/
   $$ |$$ |  $$ |$$ |  $$/       $$ |   __ $$ |$$ |$$    $$ |$$ |  $$ |  $$ | __
   $$ |$$ \__$$ |$$ |            $$ \__/  |$$ |$$ |$$$$$$$$/ $$ |  $$ |  $$ |/  |
   $$ |$$    $$/ $$ |            $$    $$/ $$ |$$ |$$       |$$ |  $$ |  $$  $$/
   $$/  $$$$$$/  $$/              $$$$$$/  $$/ $$/  $$$$$$$/ $$/   $$/    $$$$/

by JackRichardson#8842 / 790550242151759872
''')

proxies = {'http': 'socks5://127.0.0.1:9050','https': 'socks5://127.0.0.1:9050'}

ip = f''

#web driver
def init_web_Step1():
    print('\n[+] starting the client...')
    print('\n[+] checking the tor connection...')
    result_from_tor = requests.get('https://check.torproject.org/', proxies=proxies).text #Congratulations. This browser is configured to use Tor.
    if(result_from_tor.find('Congratulations. This browser is configured to use Tor.') == 166):
        print('\n[+] the check was successful, initializing the web driver...')
        init_web_Step2()
    else:
        print('\n[!] the check was unsuccessful! please check config file or internet connection...')
        sys.exit(0);

def init_web_Step2():
    print('\n[+] initializing the launch of the web interface...')
    profile = webdriver.FirefoxProfile()
    profile.set_preference('executable_path', r"WebDriver\\firefox.exe") #WebDriver\\firefox.exe

    profile.set_preference('network.proxy.type', 1)

    profile.set_preference('network.dns.blockDotOnion', False)
    profile.set_preference('network.dns.forceResolve', False)
    profile.set_preference('network.dns.localDomains', False)
    profile.set_preference('network.dns.offline-localhost', False)
    profile.set_preference('network.dns.get-ttl', False)
    profile.set_preference('network.dns.disablePrefetchFromHTTPS', False)
    profile.set_preference('network.cookie.cookieBehavior', 2)

    profile.set_preference('browser.cache.disk.enable', False)
    profile.set_preference('browser.cache.memory.enable', False)
    profile.set_preference('browser.cache.offline.enable', False)

    profile.set_preference('javascript.enabled', False)

    profile.set_preference('network.proxy.socks_remote_dns', True)
    profile.set_preference('network.proxy_dns', True)
    profile.set_preference('network.proxy.socks', '127.0.0.1')
    profile.set_preference('network.proxy.socks_port', 9050)
    profile.set_preference('network.proxy.socks_version', 5)
    profile.set_preference('network.proxy.https', '127.0.0.1')
    profile.set_preference('network.proxy.https_port', 9050)

    profile.set_preference('driver.privatebrowsing.autostart', True)

    browser = webdriver.Firefox(firefox_profile=profile, executable_path=r"WebDriver\\firefox.exe")

    browser.get("https://duckduckgo.com")

    def new_identity(port):
        with Controller.from_port(port=port) as controller:
            controller.authenticate(password="dXF9r5ZVuWR0")
            controller.signal(Signal.NEWNYM)

    while True:
        cmd = input('\n> ')

        if(cmd == "exit"):print('\n[+] good by! thanks for using tor client :3');browser.quit();sys.exit(0)
        if(cmd == "ni"):print('\n[+] getting a new identity...');new_identity(9051)
        if(cmd == "help"):print('\n[+] commands - \n exit - stop webdriver and close the tor client \n ni - you will get a new identity \n popen - open new page, accept only 1 argument! \n [ONLY FOR PRO USERS!] execute - runs the code on the page(javascript), accepts only 1 argument! | can run code to page if opened by browser.get! \n tc - print captured traffic \n clear - clear the console')
        if(cmd.find("popen") != "-1"):
            if cmd.split(" ")[0] == 'popen':pagetoopen = ' '.join(cmd.split(" ")[1:]);browser.get(pagetoopen);print('\n[+] opening a new link - ', pagetoopen)
        if(cmd.find("execute") != "-1"):
            if cmd.split(" ")[0] == 'execute':execcode = ' '.join(cmd.split(" ")[1:]);browser.execute_script(execcode);print('\n[+] executed code - ', execcode)
        if(cmd == "tc"):
            for request in browser.requests:
                if request.response:
                    print('\n\b[~] traffic captured - ', request.url, request.response.status_code, request.response.headers['Content-Type'])
        if(cmd == "clear"):os.system('cls')

#find func
def contains_word(s, w):
    return (' ' + w + ' ') in (' ' + s + ' ')

#tor launcher
p = Popen(["Tor\\tor.exe", "-f", "Tor\\torrc"], stdout=PIPE)

for line in iter(p.stdout.readline, ''):
    linedecoded = line.decode("utf-8")
    if(contains_word(linedecoded, 'Bootstrapped 100%')):print('\n[+] tor started!');init_web_Step1(),
p.stdout.close()

#debugs
'''
if(linedecoded != ""):print("\n[debug] Tor output ->", linedecoded);
print("\n[debug] find ->", contains_word(linedecoded, 'Bootstrapped 100%'));
'''