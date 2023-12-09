import mysql.connector
mysql = mysql.connector

class Data():
    def __init__(self) -> None:
        self.dbConfig = {
            'host': 'localhost',
            'user': 'root',
            'password': '1234',
            'database': 'trivselsinitiativ',
            'port': 3306
        }

    def connect_DB(self):
        mydb = mysql.connect(
            host = self.dbConfig['host'],
            user = self.dbConfig['user'],
            password = self.dbConfig['password'],
            database = self.dbConfig['database'],
            port = self.dbConfig['port']
        )

        return mydb

    def close_DB(self, mydb):
        mydb.close()


    def read(self):
        pass

    def write(self, data_dict):
        mydb = self.connect_DB()
        
        mycursor = mydb.cursor()

        tables_list = list(data_dict.keys())

        for table in tables_list:
            
            columns_list = list(data_dict[table].keys())
            columns_str = ",".join(str(element) for element in columns_list)

            values_list = columns_list = list(data_dict[table].values())
            values_str = ",".join(str(element) for element in values_list)

            
            sql = f"INSERT INTO {table} ({columns_str}) VALUES ({values_str})"  
            
            mycursor.execute(sql)

        mydb.commit()

        self.closeDB(mydb)


    def delete(self):
        pass


data_dict = {
    'employee' : {
        'gender': "'male'",
        'age' : 54,
        'occupation' : "'Doctor'"
    },
    'activity' : {
        'activity_level' : 5,
        'daily_steps' : 10000
    },
    'sleep' : {
        'sleep_duration' : 7.6,
        'sleep_quality' : 5,
        'sleep_disorder' : 'None'
    },
    'health' : {
        'stess_levl' : 6,
        'bmi_category' : "'Normal'",
        'blood_pressure' : "'125/80 '",
        'hear_rate' : 70
    }
}


if __name__ == "__main__":
    data = Data()
    data.write(data_dict)