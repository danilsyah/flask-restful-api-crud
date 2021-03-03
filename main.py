from flask import Flask
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


@app.route('/books', methods=['GET'])
def book_list():
    books = Books.query.all()
    books = [serialize_book_detail(book) for book in books]
    return response_success({'result': books})


@app.route('/books/<book_id>', methods = ['GET'])
def book_detail(book_id):
    book = Books.query.filter_by(id=book_id)
    book = book.first()

    if book == None:
        return 

    book = serialize_book_detail(book)
    return response_success({'result': book})


if __name__ == '__main__':
    app.run(debug=True)
