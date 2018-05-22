import MySQLdb
from DBUtils.PersistentDB import PersistentDB
from bs4 import BeautifulSoup
import argparse


def simpan(user, tanggal, waktu, detail, jenis, staff, pendapatan):
    pool = PersistentDB(MySQLdb, host='103.229.72.65', user='k8033228_noname', passwd='D4didudadu', db='k8033228_tekonet')
    connection = pool.connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    try:
        query = "INSERT INTO pemasukan(user,tanggal,waktu,detail,jenis,staff,pendapatan) VALUES ('{}','{}','{}','{}','{}','{}','{}')".format(
            user, tanggal, waktu, detail, jenis, staff, pendapatan)

        cursor.execute(query)
        connection.commit()
    except:
        connection.rollback()
        raise
    finally:
        connection.close()


def cek(tanggal, waktu):
    dbmysql = MySQLdb.connect(host='103.229.72.65', user='k8033228_noname', passwd='D4didudadu', db='k8033228_tekonet')
    cur = dbmysql.cursor()
    cur.execute("SELECT tanggal, waktu FROM pemasukan WHERE tanggal='{}' and waktu='{}'".format(tanggal, waktu))
    return cur.rowcount


parser = argparse.ArgumentParser()
parser.add_argument('-d', '--dir', help='directory file', required=True)
args = parser.parse_args()
dir = args.dir

source = dir
file = open(source, 'r')
data = file.read()
soup = BeautifulSoup(data, 'lxml')

data = soup.select('tr')
for i in data:
    try:
        user = i.select('td')[0].text
        tanggal = i.select('td')[1].text.split('-')
        tanggal = tanggal[2] + '-' + tanggal[1] + '-' + tanggal[0]
        waktu = i.select('td')[2].text
        ds = i.select('td')[3].text
        if i.select('td')[3].text == 'Order':
            detail = 'service'
            jenis = 'beli minum'
        else:
            detail = 'main'
            jenis = i.select('td')[3].text
        pendapatan = i.select('td')[5].text.replace(',', '')
        staff = i.select('td')[6].text
        if (tanggal == '' and waktu == '' and staff == '' and user == '' and ds == 'Total: '):
            print 'kosong tanggal'
        else:
            if cek(tanggal, waktu) == 0:
                simpan(user, tanggal, waktu, jenis, detail, staff, pendapatan)
                print 'data di tambah',tanggal
            else:
                print 'sudah ada data', tanggal
    except:
        pass
