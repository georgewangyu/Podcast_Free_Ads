import pymysql

#conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='QWop123@')
#cur.execute("CREATE DATABASE fingerprintsDB")
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='QWop123@', db= 'fingerprintsDB')
cur = conn.cursor()
#cur.execute("CREATE TABLE Fingerprints(id int, LastName varchar(32), FirstName varchar(32), DepartmentCode int)")

with conn:
    with conn.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `Fingerprints` (`id`, `LastName`) VALUES (%s, %s)"
        cursor.execute(sql, ('19233', 'Wang'))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    conn.commit()

    with conn.cursor() as cursor:
        # Read a single record
        sql = "SELECT `id`, `LastName` FROM `Fingerprints`"
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)

#print(cur.description)
#print()

#for row in cur:
#    print(row)

#cur.close()
#conn.close()