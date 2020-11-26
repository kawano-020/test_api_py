from flask import Flask, jsonify, make_response, abort
import pymysql, pymysql.cursors
app = Flask(__name__)

def get_data(sql):
  connection = pymysql.connect(host='192.168.3.50',
                             port=3306, 
                             user='orca',
                             password='Password',
                             db='flutter_db',
                             charset='utf8',
                             # Selectの結果をdictionary形式で受け取る
                             cursorclass=pymysql.cursors.DictCursor)
  try:
      with connection.cursor() as cursor:
          cursor.execute(sql)
          db_data = cursor.fetchall()
  finally:
      connection.close()
  if db_data:
    return jsonify({"list":db_data})


@app.route("/")
def get_all():
  return make_response(get_data("SELECT * FROM test"))

@app.route("/<int:id>")
def get_on_id(id):
  return make_response(get_data("SELECT subject, content, date FROM test WHERE id =" + str(id)))

@app.route("/search/<string:word>")
def get_search(word):
  return make_response(get_data("SELECT subject, content, date FROM test WHERE subject LIKE '%" + word + "%'"))

@app.errorhandler(404)
def error404(error):
  return "URLに誤りがあります。\n"+ format(error),404

@app.errorhandler(500)
def error500(error):
  return "該当するデータがありません。\n" + format(error),500

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)