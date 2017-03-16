import psycopg2
import psycopg2.sql as sql
from datetime import datetime

def create_snapshot(date_string):
        conn = psycopg2.connect(dbname='socialmedia', user='postgres')
        c = conn.cursor()

        ts = datetime.strptime(date_string, '%Y-%m-%d').strftime("%Y%m%d")

        create_table_statement = '''
        CREATE TABLE {table_name} AS
            SELECT
              reg.userid,
              reg.tmstmp AS registration_date,
              max(l.tmstmp) AS last_login,
              count(l.userid) AS logins_7d,
              sum(CASE WHEN
                l.type='mobile' AND l.tmstmp BETWEEN timestamp %(ts)s - interval '7 days' AND %(ts)s
                  THEN 1
                ELSE 0
              END) AS logins_7d_mobil,
              sum(CASE WHEN
                l.type='web' AND l.tmstmp BETWEEN timestamp %(ts)s - interval '7 days' AND %(ts)s
                  THEN 1
                ELSE 0
              END) AS logins_7d_web,
              (reg.userid IN (SELECT userid FROM optout)) AS opt_out
            FROM registrations reg
            LEFT JOIN logins l ON l.userid=reg.userid
            GROUP BY reg.userid, reg.tmstmp
            ORDER BY logins_7d;
        '''

        # Add the table name, then add the ts variable safely.
        t_name = "logins_7d_{}".format(ts)
        injection_safe = sql.SQL(create_table_statement).format(table_name=sql.Identifier(t_name))
        c.execute(injection_safe, {'ts': date_string})

        conn.commit()
        conn.close()
