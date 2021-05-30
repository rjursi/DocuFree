import sqlite3
import os, sys
import datetime



def InsertLog(filepath, detect_result):

        sql_insert = ''' INSERT INTO datelog(log_text, datect, DateInserted) 
                        VALUES (?,?,?) '''
        
        values = (filepath, detect_result, datetime.datetime.now())
        mainPath = os.path.dirname(sys.executable)
        con = sqlite3.connect(os.path.join(mainPath, 'test.db'))
        cur = con.cursor()
        cur.execute(sql_insert, values)
        con.commit()
        