from flask import Flask

from views.depts import depts_view
from views.questionaire import qs_view
from views.member import member_view



app = Flask(__name__)
app.register_blueprint(depts_view)
app.register_blueprint(qs_view)
app.register_blueprint(member_view)

if __name__ == '__main__':
    app.config["JSON_AS_ASCII"] = False
    app.run(host='0.0.0.0', port=8000)
