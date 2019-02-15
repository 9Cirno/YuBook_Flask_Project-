from app import create_app


app = create_app()


@app.route('/hello')
def hello():
    # response
    # content-type = text/html
    headers = {
        'content-type':'text/html'
        # redirection: 'location':'http://www.google.com'
    }

    return '<head><meta charset="UTF-8"></head>', 301, headers


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)
