'''
Created on 6 May 2013

@author: Ali
'''
import mcquery
import time
from __future__ import print_function
import json
from lxml import etree as ET
from test.test_iterlen import len
from _pyio import open

_adminPlus = set(['pwego', 'zachbora', 'lakersreloaded', 'sycoinc'])
_admin = set(['goodman415', 'rockgeek', 'hypuhrr', 'iamtylerharlow'])
_staff = set(['coolmankimo', 'iandrum', 'hemglassen', 'greytopher', 'nic1010', 'moviemaker2', 'xcaliber287', 'steblam', 'mr_marc', 'narugetsu', 'llama118'])
_retired = set(['littleredcow', 'pitfallingpat', 'goldengrams', 'salehewan', 'phillies'])
_artisan= set(['fumster101', 'sivert17', 'wap'])
_architect= set(['flamin_scotsman', 'stamog', 'eviil'])

host = 'mc.pwegoable.com'
port = 25565
file = 'mc.pwegoable.com.playerlog'

if __name__ == '__main__':
    print('Ctrl-C to exit')
    
    
    print("Connecting...")
    q = mcquery.MCQuery(host, port)
    print("Connected.")
    
    f = open(file=file, mode='r+')
    
    while True:
        query=json.loads(q.full_stat().replace(": ", ":").replace("'", '"').replace("\xa7", "§"))
        lowercasePlayers =  [x.lower() for x in query['players']]
        try:
            tree = ET.parse(file)
        except:
            tree = ET.Element('logfile')
        root = tree.getroot()
        logentry = ET.SubElement ( root, 'logentry' )
        datetime = ET.SubElement( logentry, 'datetime')
        datetime.text = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        players = ET.SubElement( logentry, 'datetime')
        players.text = query['numplayers']
        
        count =  ET.SubElement(logentry, 'count')
        adminPlusCount = ET.SubElement(count, 'admin+')
        adminPlusCount.text = len(_adminPlus.intersection(lowercasePlayers))
        adminCount = ET.SubElement(count, 'admin')
        adminCount.text = len(_admin.intersection(lowercasePlayers))
        staffCount = ET.SubElement(count, 'staff')
        staffCount.text = len(_staff.intersection(lowercasePlayers))
        retiredCount = ET.SubElement(count, 'retired')
        retiredCount.text = len(_retired.intersection(lowercasePlayers))
        artisanCount = ET.SubElement(count, 'artisan')
        artisanCount.text = len(_artisan.intersection(lowercasePlayers))
        architectCount = ET.SubElement(count, 'architect')
        architectCount.text = len(_architect.intersection(lowercasePlayers))
        
        for name in _adminPlus.intersection(lowercasePlayers):
            ET.SubElement(logentry, 'admin+').text = name
        
        for name in _admin.intersection(lowercasePlayers):
            ET.SubElement(logentry, 'admin').text = name
        
        for name in _staff.intersection(lowercasePlayers):
            ET.SubElement(logentry, 'staff').text = name
            
        for name in _retired.intersection(lowercasePlayers):
            ET.SubElement(logentry, 'retired+').text = name
        
        for name in _artisan.intersection(lowercasePlayers):
            ET.SubElement(logentry, 'artisan+').text = name   
        
        for name in _architect.intersection(lowercasePlayers):
            ET.SubElement(logentry, 'architect').text = name 
        
        print(ET.tostring(root, pretty_print=True, xml_declaration=True))
        
        tree = ET.ElementTree(root)
        tree.write(file, pretty_print=True, xml_declaration=True)
        
        time.sleep(180)
