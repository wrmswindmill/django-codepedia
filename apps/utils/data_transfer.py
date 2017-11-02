import pymysql
connection = pymysql.connect(host='127.0.0.1',
                             port=3306,
                             user='root',
                             password='111111',
                             db='code_pedia',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)
connection.autocommit(False)
connection2 = pymysql.connect(host='127.0.0.1',
                             port=3306,
                             user='root',
                             password='111111',
                             db='code_pedia_1',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

cursor = connection.cursor()
cursor2 = connection2.cursor()
show_tabel_sql = '''show tables'''
cursor.execute(show_tabel_sql)
all_table_dict = cursor.fetchall()
all_tables = [table['Tables_in_code_pedia'] for table in all_table_dict ]

flag = [False for i in range(0, len(all_tables))]
while False in flag:
    for i in range(0, len(all_tables)):
        table = all_tables[i]
        # query_sql = '''select * from %s ''' % (table)
        # cursor.execute(query_sql)
        # all_items = cursor.fetchall()
        # for item in all_items:
        #     sql = "insert into " + table + " values"
        #     cursor2.execute('insert into %s * from ')



        sql = "select * from " + table + " limit 1"
        cursor2.execute(sql)
        items = cursor2.fetchall()
        if len(items) > 0:
            flag[i] = True
            continue
        try:
            sql = "insert ignore into code_pedia_1." + table +' select * from code_pedia.' +table
            cursor.execute(sql)
            connection.commit()
        except Exception as e:
            print(e)
            connection.rollback()
            continue

        flag[i] = True


