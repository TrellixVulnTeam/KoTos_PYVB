import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os
import datetime
import time
import utils

ADDON      = xbmcaddon.Addon(id='plugin.video.ntv')
recordPath = xbmc.translatePath(os.path.join(ADDON.getSetting('record_path')))

def rtmpdumpFilename():
    quality = ADDON.getSetting('os')
    if quality == '0':
        return 'androidarm/rtmpdump'
    elif quality == '1':
        return 'android86/rtmpdump'
    elif quality == '2':
        return 'atv1linux/rtmpdump'
    elif quality == '3':
        return 'atv1stock/rtmpdump'
    elif quality == '4':
        return 'atv2/rtmpdump'
    elif quality == '5':
        return 'ios/rtmpdump'
    elif quality == '6':
        return 'linux32/rtmpdump'
    elif quality == '7':
        return 'linux64/rtmpdump'
    elif quality == '8':
        return 'osx106/rtmpdump'
    elif quality == '9':
        return 'osx107/rtmpdump'
    elif quality == '10':
        return 'pi/rtmpdump'
    elif quality == '11':
        return 'win/rtmpdump.exe'
    elif quality == '12':
        return '/usr/bin/rtmpdump'
        
def libPath():
    quality = ADDON.getSetting('os')
    if quality == '0':
        return os.path.join(ADDON.getAddonInfo('path'),'rtmpdump', 'androidarm')
    elif quality == '1':
        return os.path.join(ADDON.getAddonInfo('path'),'rtmpdump', 'android86')
    elif quality == '2':
        return os.path.join(ADDON.getAddonInfo('path'),'rtmpdump', 'atv1linux')
    elif quality == '3':
        return os.path.join(ADDON.getAddonInfo('path'),'rtmpdump', 'atv1stock')
    elif quality == '4':
        return os.path.join(ADDON.getAddonInfo('path'),'rtmpdump', 'atv2')
    elif quality == '5':
        return os.path.join(ADDON.getAddonInfo('path'),'rtmpdump', 'ios')
    elif quality == '6':
        return os.path.join(ADDON.getAddonInfo('path'),'rtmpdump', 'linux32')
    elif quality == '7':
        return os.path.join(ADDON.getAddonInfo('path'),'rtmpdump', 'linux64')
    elif quality == '8':
        return os.path.join(ADDON.getAddonInfo('path'),'rtmpdump', 'osx106')
    elif quality == '9':
        return os.path.join(ADDON.getAddonInfo('path'),'rtmpdump', 'osx107')
    elif quality == '10':
        return os.path.join(ADDON.getAddonInfo('path'),'rtmpdump', 'pi')
    elif quality == '11':
        return 'None'   
    elif quality == '12':
        return '/usr/bin/'

if xbmc.getCondVisibility('system.platform.linux'):
    for dirpath, dirnames, filenames in os.walk(os.path.join(ADDON.getAddonInfo('path'),'rtmpdump')):
        for filename in filenames:
            path = os.path.join(dirpath, filename)
            os.chmod(path, 0777) 


def runCommand(cmd, libpath = None, module_path = './'):
   
    from subprocess import Popen, PIPE, STDOUT

    # get the list of already defined env settings
    env = os.environ
    if (libpath):
        # add the additional env setting
        envname = "LD_LIBRARY_PATH"
        if (env.has_key(envname)):
            env[envname] = env[envname] + ":" + libpath
        else:
            env[envname] = libpath

        envname = "DYLD_LIBRARY_PATH"
        if (env.has_key(envname)):
            env[envname] = env[envname] + ":" + libpath
        else:
            env[envname] = libpath

    if (env.has_key('PYTHONPATH')):
        env['PYTHONPATH'] = env['PYTHONPATH']+':' + module_path
    else:
        env['PYTHONPATH'] = module_path
                    
    try:
        print 'env[PYTHONPATH]        = ' + env['PYTHONPATH']
        print 'env[LD_LIBRARY_PATH]   = ' + env['LD_LIBRARY_PATH']
        print 'env[DYLD_LIBRARY_PATH] = ' + env['DYLD_LIBRARY_PATH']
    except:
        pass

    subpr = Popen(cmd, shell=True, env=env, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        
    x = subpr.stdout.read()
    while subpr.poll() == None:
        time.sleep(2)
        x = subpr.stdout.read()  

    #try:        
    #    print "lines_stdout: " + str(subpr.stdout.readlines())
    #    print "lines_stderr: " + str(subpr.stderr.readlines())    
    #except:
    #    pass

import net
from hashlib import md5  
import json  
net=net.Net()

datapath = xbmc.translatePath(ADDON.getAddonInfo('profile'))
cookie_path = os.path.join(datapath, 'cookies')

loginurl = 'http://www.ntv.mx/index.php?c=3&a=0'
username    =ADDON.getSetting('user')
password = md5(ADDON.getSetting('pass')).hexdigest()


data     = {'email': username,
                                        'psw2': password,
                                        'rmbme': 'on'}
headers  = {'Host':'www.ntv.mx',
                                        'Origin':'http://www.ntv.mx',
                                        'Referer':'http://www.ntv.mx/index.php?c=3&a=0'}
                                        
#create cookie
html = net.http_POST(loginurl, data, headers)
cookie_jar = os.path.join(cookie_path, "ntv.lwp")
if os.path.exists(cookie_path) == False:
        os.makedirs(cookie_path)
net.save_cookies(cookie_jar)

#set cookie to grab url
net.set_cookies(cookie_jar)

duration = sys.argv[4]
cat      = sys.argv[1]
title    = sys.argv[5]

def Numeric():
        dialog = xbmcgui.Dialog()
        keyboard=dialog.numeric(0, 'Minutes To Record?')
        return keyboard
    
def NAME():
        search_entered = ''
        keyboard = xbmc.Keyboard(search_entered, 'Please Enter Programme Name')
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_entered = keyboard.getText()
            if search_entered == None:
                return False          
        return search_entered  

if 'n a' in title:
    amount=int(Numeric())
    duration =amount * 60
    title=NAME()+' - ['+datetime.datetime.today().strftime('%d-%m-%Y')+']'

url      = 'http://www.ntv.mx/index.php?c=6&a=0&mwAction=content&xbmc=1&mwData={"id":%s,"type":"tv"}' % cat
link     = net.http_GET(url,headers={"User-Agent":"NTV-XBMC-" + ADDON.getAddonInfo('version')}).content

data     = json.loads(link)

rtmp     = data['src']

rtmp  = '%s' % (rtmp)

cmd  =  os.path.join(ADDON.getAddonInfo('path'),'rtmpdump', rtmpdumpFilename())
cmd += ' -V --stop ' + str(duration) 
cmd += ' --live '
cmd += ' --flv "' + recordPath + re.sub('[:\\/*?\<>|"]+', '', title) + '.flv"'
cmd += ' --rtmp "' + rtmp
cmd += '"'

print "Record.py command:"
print cmd


utils.notification('Recording %s started' % title)

if ADDON.getSetting('os')=='11':
    runCommand(cmd, libpath=None)
else:
    libpath = libPath()
    runCommand(cmd, libpath=libpath)

utils.notification('Recording %s complete' % title)
