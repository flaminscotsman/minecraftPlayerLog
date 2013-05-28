#!/bin/python

'''
Created on 6 May 2013

@author: Ali
'''
import mcquery
import datetime
from __future__ import print_function
import MySQLdb as mdb

host = 'mc.pwegoable.com'
port = 25565

mysqlHost = 'localhost'
mysqlUser = 'minecraftLogging'
mysqlPass = 'password'
mysqlDB   = 'minecraftLogging'

mainTable = 'pwegoableLogs'
userTable = 'pwegoableUsers'
relationshipTable = 'pwegoableMapping'

mainTableQuery = "INSERT INTO `%s` (`id`, `time`, `count`) VALUES (NULL, `%s`, %s)"
mappingQuery = "INSERT INTO `%s` (`timeID`, `userID`) SELECT %s, memberID FROM %s where `username` IN (%s)"
DEBUG = False

if __name__ == '__main__':
    if DEBUG:
        print('Ctrl-C to exit')
        print("Connecting...")
        
    q = mcquery.MCQuery(host, port)
    
    if DEBUG:
        print("Connected.")
        print("Querying server...")
        
    query = q.full_stat()
    time = datetime.datetime.utcnow()
    
    if DEBUG:
        print("Query completed.")
        print("Connecting to mySQL server")    
    con = mdb.connect(mysqlHost, mysqlUser,  mysqlPass, mysqlDB);
    
    
    with con:
        cursor = con.cursor()
        cursor.execute(mainTableQuery, (mainTable, time.strftime('%Y-%m-%d %H:%M:%S'), query['numplayers']))
        cursor.execute(mappingQuery, (relationshipTable, cursor.lastrowid, userTable,  ", ".join(["'" + playername + "'" for playername in query['players']])))
        cursor.commit()