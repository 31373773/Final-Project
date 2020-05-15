from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'ZillowData'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Zillow  Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM TableZillow')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, houses=result)


@app.route('/view/<int:house_id>', methods=['GET'])
def record_view(house_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM TableZillow WHERE id=%s', house_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', house=result[0])


@app.route('/edit/<int:house_id>', methods=['GET'])
def form_edit_get(house_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM TableZillow WHERE id=%s', house_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', house =result[0])


@app.route('/edit/<int:house_id>', methods=['POST'])
def form_update_post(house_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Indx'), request.form.get('LivingSpace'), request.form.get('Beds'),
                 request.form.get('Baths'), request.form.get('Zip'),
                 request.form.get('Yr'), request.form.get('LstPrice'), house_id)
    sql_update_query = """UPDATE tblCitiesImport t SET t.fldName = %s, t.fldLat = %s, t.fldLong = %s, t.fldCountry = 
    %s, t.fldAbbreviation = %s, t.fldCapitalStatus = %s, t.fldPopulation = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/houses/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New House Form')


@app.route('/houses/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Indx'), request.form.get('LivingSpace'), request.form.get('Beds'),
                 request.form.get('Baths'), request.form.get('Zip'),
                 request.form.get('Yr'), request.form.get('LstPrice'))
    sql_insert_query = """INSERT INTO TableZillow (Indx,LivingSpace,Beds,Baths,Zip,Yr,LstPrice) VALUES (%s, %s,%s, %s,%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/delete/<int:house_id>', methods=['POST'])
def form_delete_post(house_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM TableZillow WHERE id = %s """
    cursor.execute(sql_delete_query, house_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/houses', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM TableZillow')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/houses/<int:house_id>', methods=['GET'])
def api_retrieve(house_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM TableZillow WHERE id=%s', house_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/houses/', methods=['POST'])
def api_add() -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/houses/<int:house_id>', methods=['PUT'])
def api_edit(house_id) -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/houses/<int:house_id>', methods=['DELETE'])
def api_delete(house_id) -> str:
    resp = Response(status=210, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)