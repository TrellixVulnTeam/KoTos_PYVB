#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import xbmc, xbmcgui
from resources.lib import common

def start_rytec_service():
    from resources.lib import rytec
    print '[Rytec EPG Downloader]: rytec service started'
    descriptions = common.get_descriptions()
    sources_list = None
    merge = False
    for description in descriptions:
        ret = False
        epg_url = common.get_description_url(description)
        if epg_url:
            ret = common.load_local_xml(epg_url)
            if ret:
                print '[Rytec EPG Downloader]: no epg update needed', description
            else:
                ret = rytec.download_epg(epg_url)
                if ret: merge = True
        if not ret:
            if not sources_list: sources_list = rytec.get_sources_list()
            if sources_list:
                ret = rytec.get_epg(sources_list, description)
                if ret:
                    merge = True
                else:
                    xbmc.executebuiltin('Notification(could not download epg data,)')
                    print '[Rytec EPG Downloader]: could not download epg data', description
            else:
                xbmc.executebuiltin('Notification(could not download sources list,)')
                print '[Rytec EPG Downloader]: could not download sources list'
    if merge and len(descriptions) > 1: 
        try:
            common.merge_epg()
        except Exception, e:
            xbmc.executebuiltin('Notification(could not merge epg,)')
            print '[Rytec EPG Downloader]: could not merge epg', e

def service():
    a = False
    while (not xbmc.abortRequested):
        if not (xbmc.Player().isPlaying() or xbmc.getCondVisibility('Library.IsScanningVideo')):
            if common.download_allowed(a):
                if not common.blocked(a):
                    start_rytec_service()
            else:
                if not a: 
                    xbmc.executebuiltin('Notification(epg download currently not allowed,)')
            a = True
        xbmc.sleep(1000)

if common.get_xml_path() and common.get_activation_code():
    try:
        if sys.argv[1:][0] == 'manual_download':
            dialog = xbmcgui.Dialog()
            ret = dialog.yesno('Rytec EPG Downloader', 'Start Manual Download')
            if ret:
                start_rytec_service()
                ok = dialog.ok('Rytec EPG Downloader', 'Manual Download Finished')
    except:
        service()