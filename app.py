import os
from flask import *
from firebase_admin import credentials, firestore, initialize_app
import pdb
# Initialize Flask app
app = Flask(__name__)

# Initialize Firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('users')

@app.route('/')
def index():
    return render_template('index.html')

# kt db di
@app.route('/add', methods=['GET'])
def create():
    try:
        db = firestore.client()
        # [START quickstart_add_data_one]
        doc_ref = db.collection(u'users').document(u'huy')
        #pdb.set_trace()
   
        doc_ref.set({
            u'maso': u'user003',
            u'first': u'Ada',
            u'last': u'Lovelace',
            u'born': 1815
        })
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/list', methods=['GET'])
def read():
 
    try:
        # Check if ID was passed to URL query
        todo_id = request.args.get('maso')
        # dong nay chap nhan tham so ten 'maso'
        if todo_id:
            # nay no lay tren truong documents
            todo = todo_ref.document(todo_id).get()
            return jsonify(todo.to_dict()), 200
        else:
            all_todos = [doc.to_dict() for doc in todo_ref.stream()]
            return jsonify(all_todos), 200
    except Exception as e:
        return f"An Error Occured: {e}"
        
        

@app.route('/update', methods=['PUT'])
def update():
    try:
        # B4: Server xu ly tham so
        maso = request.form.get('maso')
        first = request.form.get('first')
        last = request.form.get('last')
        born = request.form.get('born')
        # pdb.set_trace()
        # B5: Server edit
        # get record co ma so = input
        doc_ref = db.collection(u'users').document('John')
        #pdb.set_trace()

        if doc_ref is not None:
               # tim thay du lieu
            doc_ref.set({
                u'first': first,
                u'last': last,
                u'born': born
            })
            data = {"success": True, "message": u"Update thanh cong"}
        else:
            # ko tim thay
            data = {"success": False, "message": u"Update that bai, khong tim thay record"}
        # server backend se tra ve du lieu
        
        return jsonify(data), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/delete', methods=['GET', 'DELETE'])
def delete():
    try:
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

if __name__=='__main__':
    app.run(threaded=True, port=5000)
