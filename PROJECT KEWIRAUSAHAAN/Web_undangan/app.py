from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector

app = Flask(__name__, template_folder="../forend_project", static_folder="../statistic")
app.secret_key = "kunci_rahasia_nauvali"

# Konfigurasi Database MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',       # Sesuaikan dengan user phpMyAdmin Anda
    'password': '',       # Sesuaikan dengan password phpMyAdmin Anda (kosongkan jika default)
    'database': 'db_undangan'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pesan', methods=['POST'])
def pesan():
    if request.method == 'POST':
        nama = request.form['nama']
        whatsapp = request.form['whatsapp']
        jenis = request.form['jenis']
        catatan = request.form['catatan']

        conn = get_db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO pesanan (nama_kustomer, no_whatsapp, jenis_undangan, catatan) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (nama, whatsapp, jenis, catatan))
        conn.commit()
        cursor.close()
        conn.close()

        flash("Pesanan berhasil dikirim! Kami akan segera menghubungi Anda melalui WhatsApp.")
        return render_template('index.html')
    
# Username dan Password rahasia untuk Admin
ADMIN_USERNAME = "admin_kisahkita"
ADMIN_PASSWORD = "123"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'admin_logged_in' in session:
        return redirect(url_for('admin'))

    if request.method == 'POST':
        username_input = request.form['username']
        password_input = request.form['password']

        if username_input == ADMIN_USERNAME and password_input == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin'))
        else:
            flash("Username atau Password salah!", "error")
            return redirect(url_for('login'))
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Ini adalah sistem untuk MENGELUARKAN admin
    session.pop('admin_logged_in', None)
    return redirect(url_for('login'))

@app.route('/admin')
def admin():
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pesanan ORDER BY tanggal_pesan DESC")
    data_pesanan = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('admin.html', pesanan=data_pesanan)

@app.route('/acc/<int:id_pesanan>')
def acc_pesanan(id_pesanan):
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE pesanan SET status_pesanan = 'Selesai' WHERE id = %s", (id_pesanan,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/delete/<int:id_pesanan>')
def delete_pesanan(id_pesanan):
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pesanan WHERE id = %s", (id_pesanan,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('admin'))
if __name__ == '__main__':
    app.run(debug=True)