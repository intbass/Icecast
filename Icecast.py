#!/usr/bin/env python

import xml.etree.ElementTree as ET
import requests
from requests.exceptions import ConnectionError

# global vars
headers = {"User-agent": "Mozilla/5.0"}
httptimeout = 2.0


class IcecastError(Exception):
    pass


class IcecastServer:
    """Details relating to an Icecast server."""
    def __init__(self, name, hostname, port, username, password):
        self.Name = name
        self.Hostname = hostname
        self.Port = port
        self.UserName = username
        self.Password = password
        self.Mounts = []

        url = "http://{}:{}/admin/stats.xml".format(hostname, port)
        try:
            req = requests.get(url, auth=(username, password),
                               headers=headers, timeout=httptimeout)
        except ConnectionError as e:
            raise IcecastError(e)
        if req.status_code == 401:
            raise IcecastError("Authentication Failed.")
        elif req.status_code != 200:
            raise IcecastError("Unknown Error.")
        try:
            self.IceStats = ET.fromstring(req.text)
        except:
            raise IcecastError("Error parsing xml.")

        # Common attributes
        self.Admin = self.IceStats.find('admin').text
        self.ClientConnections = self.IceStats.find('client_connections').text
        self.Clients = self.IceStats.find('clients').text
        self.Connections = self.IceStats.find('connections').text
        self.FileConnections = self.IceStats.find('file_connections').text
        self.Host = self.IceStats.find('host').text
        self.ListenerConnections = self.IceStats.find('listener_connections').text
        self.Listeners = self.IceStats.find('listeners').text
        self.Location = self.IceStats.find('location').text
        self.ServerID = self.IceStats.find('server_id').text
        self.ServerStart = self.IceStats.find('server_start').text
        self.SourceClientConnections = self.IceStats.find('source_client_connections').text
        self.SourceRelayConnections = self.IceStats.find('source_relay_connections').text
        self.SourceTotalConnections = self.IceStats.find('source_total_connections').text
        self.Sources = self.IceStats.find('sources').text
        self.Stats = self.IceStats.find('stats').text
        self.StatsConnections = self.IceStats.find('stats_connections').text

        # -kh version has special attributes
        if "-kh" in self.ServerID:
            self.BannedIPs = self.IceStats.find('banned_IPs').text
            self.KBytesRead = self.IceStats.find('stream_kbytes_read').text
            self.KBytesSent = self.IceStats.find('stream_kbytes_sent').text
            self.OutgoingBitrate = self.IceStats.find('outgoing_kbitrate').text

        # Add this server's mounts
        for mount in self.IceStats.iter('source'):
            self.Mounts.append(IcecastMount(mount, self))

class IcecastMount:
    """Details pertaining to an Icecast Mount."""
    def __init__(self, mount, server):
        self.IceStats = mount
        self.Server = server
        self.Listeners = []
        self.Name = self.IceStats.get('mount')

        url = "http://{}:{}/admin/listclients?mount={}".format(
                server.Hostname, server.Port,
                self.Name)
        try:
            req = requests.get(url, auth=(server.UserName, server.Password),
                               headers=headers, timeout=httptimeout)
        except ConnectionError as e:
            raise IcecastError(e)

        try:
            self.ListenerStats = ET.fromstring(req.text)
        except:
            raise IcecastError("Invalid Mount XML.")

        # Miscellaneous Information
        self.AudioInfo = self.IceStats.find('audio_info').text
        self.Genre = self.IceStats.find('genre').text
        self.ListenerCount = self.IceStats.find('listeners').text
        self.ListenerPeak = self.IceStats.find('listener_peak').text
        self.ListenURL = self.IceStats.find('listenurl').text
        self.MaxListeners = self.IceStats.find('max_listeners').text
        self.Public = self.IceStats.find('public').text
        self.ServerDescription = self.IceStats.find('server_description').text
        self.ServerName = self.IceStats.find('server_name').text
        self.ServerType = self.IceStats.find('server_type').text
        self.ServerURL = self.IceStats.find('server_url').text
        self.SlowListeners = self.IceStats.find('slow_listeners').text
        self.SourceIP = self.IceStats.find('source_ip').text
        self.StreamStart = self.IceStats.find('stream_start').text
        self.Title = self.IceStats.find('title').text
        self.TotalBytesRead = self.IceStats.find('total_bytes_read').text
        self.TotalBytesSent = self.IceStats.find('total_bytes_sent').text
        self.UserAgent = self.IceStats.find('user_agent').text

        # -kh version has special attributes
        if "-kh" in server.ServerID:
            self.Artist = self.IceStats.find('artist').text
            self.AudioCodecID = self.IceStats.find('audio_codecid').text
            self.Connected = self.IceStats.find('connected').text
            self.IncomingBitrate = self.IceStats.find('incoming_bitrate').text
            self.ListenerConnections = self.IceStats.find('listener_connections').text
            self.MetadataUpdated = self.IceStats.find('metadata_updated').text
            self.OutgoingKbitRate = self.IceStats.find('outgoing_kbitrate').text
            self.TotalMBytesSent = self.IceStats.find('total_mbytes_sent').text

        # Populate the Listeners list for this mount
        for listener in self.ListenerStats.iter('listener'):
            self.Listeners.append(IcecastListener(listener))


class IcecastListener:
    """An Icecast listener."""
    def __init__(self, listener):
        self.IcecastID = listener.get('id')
        self.IP = listener.findtext('IP')
        self.UserAgent = listener.findtext('UserAgent')
        self.Connected = listener.findtext('Connected')
        self.IceStats = listener