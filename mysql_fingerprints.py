import pymysql

#conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='QWop123@')
#cur.execute("CREATE DATABASE fingerprintsDB")
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='QWop123@', db= 'fingerprintsDB')
cur = conn.cursor()
cur.execute("CREATE TABLE Fingerprints(id int, timestamp int, hash varchar(40), offset int, adid int)")
cur.execute("CREATE TABLE AdSegments(id int, duration int)")


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


def addfingerprint(timestampList, hashList, offsetList, adID):
    with conn:
        with conn.cursor() as cursor:
            # Create a new record
            for i, timestamp in enumerate(timestampList):
                sql = "INSERT INTO `Fingerprints` (`timestamp`, `hash`, `offset`, `adid`) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (timestamp, hashList[i], offsetList[i], adID[i]))


def addAdSegment(durationList):
    with conn:
        with conn.cursor() as cursor:
            # Create a new record
            for int in durationList:
                sql = "INSERT INTO `AdSegments` (`durationList`) VALUES (%s)"
            cursor.execute(sql, int)




#print(cur.description)
#print()

#for row in cur:
#    print(row)

#cur.close()
#conn.close()