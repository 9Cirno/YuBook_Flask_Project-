from flask import jsonify, render_template, flash
from app.libs import helper
from app.spider.YuShuBook import YuShuBook
from app.web import web
from flask import request
from app.forms.book import SearchForm
from app.view_models.book import BookCollection
import json

@web.route('/book/search')
def search():
    '''
        q : key/isbn
        page
    '''
    # isbn 13 isbn 10
    #q = request.args['q']
    # request.args.to_dict
    # validation
    #page = request.args['page']
    form = SearchForm(request.args)
    books = BookCollection()
    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = helper.is_isbn_or_key(q)
        yushu_book = YuShuBook()

        if isbn_or_key == 'isbn':
            yushu_book.search_by_isbn(isbn_or_key)
        else:
            yushu_book.search_by_keyword(q, page)
            # API

        books.fill(yushu_book, q)
        # return json.dumps(books, default=lambda o: o.__dict__)

        #return jsonify(books.__dict__)
    else:
        flash("ERROR KEYWORD IS NOT VALID")

    return render_template('search_result.html', books)
        #return jsonify({'msg':'faileddddddd'})
    #return json.dumps(result), 200, {'content-type':'application/json'}


@web.route('/test')
def test():
    r = {
        'name':"nb",
         'age':18
    }
    flash('hello nbnb')
    return render_template('test.html', data = r)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    pass
