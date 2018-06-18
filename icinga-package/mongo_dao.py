from pymongo import MongoClient

class NotificationDao:

    def __init__(self, host, port,mongoUri=None):
        self.host = host
        self.port = port
        if mongoUri:
            self.client = MongoClient(mongoUri)    
        else:
            self.client = MongoClient(host, port)

    def get_client(self):
        return self.client

    def get_db(self):
        return self.db

    def database(self, database):
        if not database in self.client.database_names():
            print 'The requested database "{0}" is not found on client "{1}:{2}"'.format(database, self.host, self.port)
            return
        else:
            self.db = self.client[database]
            return self

    def collectn(self, collection):
        if self.db:
            if not collection in self.db.collection_names():
                print 'The requested collection "{0}" is not found in database "{1}".'.format(self.collection, self.db)
            else:
                self.collection = self.db[collection]
            return self
        else:
            print 'Invalid request for collection "{0}". No database has been selected.'.format(self.collection)
            return None

    def find(self, condition=None, lim=0):
        if isinstance(condition, dict):
            return self.collection.find(condition, {'_id': 0},timeout=False).limit(lim)
        else:
            return self.collection.find({}, {'_id': 0},timeout=False).limit(lim)

    def update(self, select_cond, update_args):
        if not update_args:
            return
        if not isinstance(select_cond, dict):
            select_cond = {}
        if self.collection:
            result = self.collection.update(
                select_cond, {'$set': update_args}, multi=False, j=True)
            print result
        else:
            print 'Invalid request. No Collection has been selected'

    def insert(self, doc):
        if self.collection:
            objid = self.collection.insert(doc)
            return objid
        else:
            print 'Invalid request. No Collection has been selected'


# sel_dict = { "ack":0 }
# update_dict = {'time':['Tue Nov 26 2013 12:07:09 GMT+0530 (India Standard Time)']}
# dao = NotificationDao()
# dao.database('work').collectn('notifications').update(sel_dict, update_dict)
