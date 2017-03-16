import psycopg2



def fetch_avg_per_type():
    # Login
    conn = psycopg2.connect('dbname=readychef user=Tyler')

    # This is pretty useful -- and required if you're doing somethign that isn't transaction based:
    # Ivan suggests this strongly.
    conn.autocommit = True
    cursor = conn.cursor()
    query = """
    with average_per_type as (
      SELECT
        type,
        AVG(price) AS avg_price
      FROM meals GROUP BY type
    )

    SELECT meals.*
    FROM meals
    JOIN average_per_type ON
      average_per_type.type=meals.type and
      meals.price > average_per_type.avg_price
    """

    cursor.execute(query);
    results = cursor.fetchall()

    cursor.close()
    conn.close()
    return results

def load_csv(conn, csv_path, table_name):
    '''
        Given a connection and an absolute path to a file and a table name
        load the data from the csv into the specified table. We assume in
        this case that the delimiter is a comma.
    '''
    cursor = conn.cursor()
    query = '''
    COPY %(table_name)s
        FROM %(file_path)s
        DELIMITER ,
        CSV;
    '''

    cursor.execute(query, {
        'file_path': path,
        'table_name': table_name
    })


cursor.execute("""
    SELECT * FROM transaction where acct_num=%(acct_num)s;
""", {"acct_num": num})
