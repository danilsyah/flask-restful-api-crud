from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storage.db'


@app.errorhandler(404)
def page_not_found(e):
    return {
        'error': 'page is not found'
    }


db = SQLAlchemy(app)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    preview = db.Column(db.Text, nullable=True)


db.create_all()


def response_success(data={}):
    default = {'status': 'ok'}
    return {**default, **data}

def response_failed(data={}):
    default = {'status': 'failed'}
    return {**default, **data}


def serialize_book_detail(book):
    return {
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'preview': book.preview,
    }

# view all data book 
@app.route('/books', methods=['GET'])
def book_list():
    books = Books.query.all()

    if len(books) == 0 :
        return response_success({'result': 'data is empty'})

    books = [serialize_book_detail(book) for book in books]
    return response_success({'result': books})


# view detail book berdasarkan id buku
@app.route('/books/<book_id>', methods = ['GET'])
def book_detail(book_id):
    book = Books.query.filter_by(id=book_id)
    book = book.first()

    if book == None:
        return response_failed({
            'message' : f'Book #{book_id} does not exist'
        })

    book = serialize_book_detail(book)
    return response_success({'result': book})


# create data book / menambahkan buku baru
@app.route('/books', methods=['POST'])
def book_add():
    req_data = request.get_json()

    book_title = req_data.get('title')
    book_author = req_data.get('author')
    book_preview = req_data.get('preview')

    book = Books(
        title = book_title,
        author = book_author,
        preview = book_preview
    )

    try:
        db.session.add(book)
        db.session.commit()
        return response_success()
    except Exception as e:
        return response_failed()


# update data book berdasarkan id
@app.route('/books/<book_id>', methods = ['PUT'])
def book_update(book_id):
    book = Books.query.filter_by(id=book_id)
    book = book.first()

    if book == None:
        return response_failed({
            'message':f'Book #{book_id} does not exist'
        })

    req_data = request.get_json()

    try:
        book.title = req_data.get('title')
        book.author = req_data.get('author')
        book.preview = req_data.get('preview')
        db.session.commit()
        return response_success()
    except Exception as e:
        return response_failed()


# endpoint delete data book berdasarkan id buku
@app.route('/books/<book_id>', methods=['DELETE'])
def book_delete(book_id):
    book = Books.query.filter_by(id=book_id)
    book = book.first()

    if book == None:
        return response_failed({
            'message': f'Book #{book_id} does not exists'
        })

    try:
        db.session.delete(book)
        db.session.commit()
        return response_success()
    except Exception as e:
        return response_failed()



if __name__ == '__main__':
    app.run(debug=True)
