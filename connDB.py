import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import sys, os, os.path
class connDB:
    
    def __init__(self):

        def resource_path(relative_path):
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            if hasattr(sys, '_MEIPASS'):
                return os.path.join(sys._MEIPASS, relative_path)
            return os.path.join(os.path.abspath("."), relative_path)

        cred = credentials.Certificate(resource_path(os.path.join("tokyo-country-300108-firebase-adminsdk-8v6yy-d5534ae12d.json")))

        try:
            firebase_admin.initialize_app(cred)
        except:
            print('already connecnt to DB')
        
        self.db = firestore.client()
    
    def initusr(self,sid, admin, canuse):
        doc_ref = self.db.collection(u'user').document(sid)
        doc_ref.set({
            u'admin': admin,
            u'canuse': canuse,
        })
    
        doc_ref = self.db.collection(u'user').document(sid).collection('selcourse').document(u'default')
        doc_ref.set({u'timestamp': firestore.SERVER_TIMESTAMP})

    def findusr(self,sid):
        doc_ref = self.db.collection(u'user').document(sid)
        doc = doc_ref.get()
        if doc.exists:
            #print(f'Document data: {doc.to_dict()}')
            return True
        else:
            #print(u'No such document!')
            return False
    
    def selOK(self,sid,course):
        doc_ref = self.db.collection(u'user').document(sid)
        doc = doc_ref.get()
        x = doc.to_dict()['canuse']
        if x > 0:
            x-=1
            doc_ref.update({u'canuse': x})
        doc_ref = self.db.collection(u'user').document(sid).collection('selcourse').document(course)
        doc_ref.set({u'timestamp': firestore.SERVER_TIMESTAMP})
    
    def chkuse(self,sid):
        doc_ref = self.db.collection(u'user').document(sid)
        doc = doc_ref.get()
        x = doc.to_dict()['canuse']
        if x <= 0:
            return True
