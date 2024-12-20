from app import create_app

__author__ = "zhujiangwei"

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
