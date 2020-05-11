from flask import Flask, render_template, request, send_from_directory, redirect
from helpers.postgresql import *
from helpers.html import *
from flask import session
import smtplib
from smtplib import *

app = Flask(__name__)
app.secret_key = 'rahasia'
 

def send_email(user, pwd, recipient, subject, body):


    FROM = user
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        return 'berhasil'
    except SMTPResponseException as e:
        return e.smtp_error

@app.route("/list_user")
def list_user():
    query = "select * from v_pengusaha"
    all_user = fetchall(query)
    return render_template('admin_page.html',all_user=all_user)

@app.route("/lupa_password", methods=['POST'] )
def lupa_password():
    email = request.form.get('email')
    query = "select count(*) as jumlah from pengusaha where email = '"+email+"'"
    from random import randrange
    password_baru = randrange(10000)
    dict_query = {
        "table":"pengusaha",
        "data":{
            "password" : password_baru
        },
        "condition":"email = '"+email+"'"
    }
    update(dict_query)

    if fetch(query)['jumlah'] > 0:
        # kirim ke email , berupa link untuk reset password yang dinamis
        subject = "Reset Password"
        body = """
            Password anda yang baru adalah {password_baru}, silahkan login dengan password ini.
        """.format(password_baru=password_baru)
        result = send_email('info@bangundigdaya.com','Pesanggrahan20191107',email,subject,body)
        return result
    else:
        return 'Email yang anda masukkan , tidak terdaftar.'

        

@app.route("/daftar", methods=['POST'])
def daftar():
    email = request.form.get('email')
    password = request.form.get('password')
    # check apakah sudah ada email ini di database, bila ada keluar pesan sudah ada
    # jika belum insert ke database
    query = "select count(*) as jumlah from pengusaha where email = '"+email+"'"
    if fetch(query)['jumlah'] > 0:
        return 'Email sudah terdaftar'
    # jika belum ada maka insert
    query = "insert into pengusaha (email,password) values ('"+email+"','"+password+"')"
    insert(query)
    return 'Berhasil di daftarkan'


@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/")
def map():
    latlong = get_latlong()

    return render_template('map.html',latlong=latlong)

@app.route("/logout")
def logout():
    import urllib.request
    # clear chache
    session.clear()
    url = request.environ['HTTP_REFERER']

    return redirect(url.replace('utama',''), code=302)

    # return redirect("/")

@app.route("/masuk",methods=['POST'])
def masuk():
    email = request.form.get('email')
    password = request.form.get('password')

    query = "select count(*) as jumlah from pengusaha where email = '"+email+"' and password = '"+password+"'"

    query_admin = "select count(*) as jumlah from configurasi where password_admin = '"+password+"'"

    if fetch(query)['jumlah'] > 0  :
        # jika yang di masukkan user kosong 
        if email == '':
            return 'Anda memasukkan email kosong!'

        # set session email
        session['email'] = email
        return 'Berhasil'
    elif fetch(query_admin)['jumlah'] > 0:

        session['email'] = email
        session['is_admin'] = True
        return 'Berhasil'

    else:
        return 'User / password yang anda masukkan salah'
    

def get_latlong():
    query = 'select * from v_pengusaha'
    hasil = fetchall(query)
    latlong = []
    for i in hasil:
        if i['latitude'] == None or i['latitude'] == 0:
            continue
        latlong.append( [ i['nama'], i['latitude'], i['longitude'] ] )
    # return latlong
    return hasil

@app.route("/utama")
def utama():

    if 'email' not in session:
        return redirect("/login")   

    latlong = get_latlong()
        
    # ambil data pengusaha
    query = "select * from pengusaha where email = '"+session['email']+"'"
    pengusaha = dict(fetch(query))
    if pengusaha['whatsapp'] != None:
        pengusaha['whatsapp'] = pengusaha['whatsapp'].replace('https://wa.me/62','')

    return render_template('utama.html',
        select_jenis_umkm=dropdown(
            query='select id,nama as name from jenis_umkm',
            name='jenis_umkm',
            label='Jenis UMKM:'
        ),

        select_child_jenis_umkm=dropdown(
            query='select id,nama as name from child_jenis_umkm',
            name='jenis_umkm_detil',
            label='Jenis UMKM Detil:'
        ),latlong=latlong,pengusaha=pengusaha,is_admin = 'is_admin' in session
    )


@app.route('/simpan', methods=['POST'])
def simpan():

    import urllib.request, json 

    placeId = request.form.get('place_id')

    key_api = 'AIzaSyDcyzudenazr_agpHvowA0rc-Jv1unIg8A'

    urlnya = "https://maps.googleapis.com/maps/api/place/details/json?placeid="+placeId+"&key="+key_api

    with urllib.request.urlopen(urlnya) as url:
        data = json.loads(url.read().decode())
        # print(data)
    whatsapp = request.form.get('whatsapp')

    # check apakah ada 0 depannya, bila ada 0 depannya maka hapus 0 nya 

    if whatsapp[0] == '0':
        whatsapp = whatsapp[1:]

    whatsapp =  'https://wa.me/62' + whatsapp
    dict_query = {
        "table":"pengusaha",
        "data":{
            "alamat" : request.form.get('alamat'),
            "email" : request.form.get('email'),
            "jenis_umkm_id" : request.form.get('jenis_umkm'),
            "child_jenis_umkm_id" : 1 if request.form.get('jenis_umkm_detil') == None else request.form.get('jenis_umkm_detil'),
            "latitude" : data['result']['geometry']['location']['lat'] if 'result' in data else 0,
            "longitude" : data['result']['geometry']['location']['lng'] if 'result' in data else 0,
            "nama" : request.form.get('nama'),
            "jumlah_stok" : request.form.get('jumlah_stok'),
            "place_id" : request.form.get('place_id'),
            "marketplace" : request.form.get('marketplace'),
            "whatsapp" : whatsapp
            
        },
        "condition":"id = "+ request.form.get('id_pengusaha')
    }
    update(dict_query)

    # request.environ['HTTP_ORIGIN']
    return redirect(request.environ['HTTP_ORIGIN']+"/utama", code=302)

    # return redirect("/utama")

@app.route('/dropdown_update', methods=['POST','GET'])
def dropdown_update():
    parent_id = request.form.get('parent_id','')
    parent_column = request.form.get('parent_column','')
    table = request.form.get('table','')
    id = request.form.get('id','id')
    name = request.form.get('name','')
    select_name = request.form.get('select_name','')
    label = request.form.get('label','')

    query='select '+id+' as id,'+name+' as name from '+table +' where '+parent_column+' ='+parent_id

    isi_dropdown = dropdown(
        query=query,
        name=select_name,
        label=label
    )

    return isi_dropdown


# @app.route('/favicon.ico')
# def favicon():
#     import os
#     return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == "__main__":
    app.run(host='0.0.0.0')
