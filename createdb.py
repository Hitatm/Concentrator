import sqlite3

conn = sqlite3.connect("test.db")

c = conn.cursor()

# create tables

c.execute('''CREATE TABLE topo
      (topoid integer primary key autoincrement, 
       synlevel int, 
       synsqnum int, 
       syntimestamp time, 
       restarttimes int,
       rtx int,
       cpu bigint,
       num_of_neighbour int,
       BeaconInterval int,
       lpm bigint,
       syntimediff int,
       voltage float,
       ParentID varchar,
       transmit bigint,
       realtimestamp varchar,
       nodetimestamp time,
       ID varchar,
       synparentID varchar,
       listen bigint)
       ''')
# realtimestamp datetime,

# save the changes
conn.commit()

# close the connection with the database
conn.close()


# {'synlevel': '1', 'synsqnum': '34', 'syntimestamp': '9:35:3', 'restarttimes': '0',
#  'rtx': '768', 'cpu': '864351', 'num_of_neighbour': '60', 'BeaconInterval': '4194', 
#  'lpm': '706855229', 'syntimediff': '-1', 'voltage': '3685', 'ParentID': '37', 'transmit': '4350', 
#  'realtimestamp': '2016-10-31_09:32:32', 'nodetimestamp': '9:32:33', 'ID': 'f4', 'synparentID': '15', 
#  'listen': '600345'}