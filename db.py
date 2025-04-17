import pymysql
db_setting={
    "host":"localhost",
    "port":3306,
    "user":"root",
    "password":"Ah03Da11La02",
    "db":"goods",
    "charset":"utf8"
}
test={"id":1,"pchomelink":"www", "pchomename":"headphone","pchomeprice":"12345"}
try:
    # 建立Connection物件
    conn = pymysql.connect(**db_setting)
    # 建立Cursor物件
    with conn.cursor() as cursor:
        clear="TRUNCATE TABLE pchome"
        command = "INSERT INTO pchome(id, pchomelink, pchomename,pchomeprice)VALUES(%s, %s, %s,%s)"
        cursor.execute(command,(test["id"],test["pchomelink"],test["pchomename"],test["pchomeprice"]))
        cursor.execute(clear)
        conn.commit()
except Exception as ex:
    print(ex)