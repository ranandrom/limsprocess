#coding:utf8
from app import app


# app.run(debug=True)

if __name__ =='__main__':
    b = True
    while (b):
        try:
            app.run()
            b = False
        except:
            k = 0