import mysql.connector
mysql = mysql.connector


import csv

class Data():
    def __init__(self) -> None:
        self.dbConfig = {
            'host': 'localhost',
            'user': 'root',
            'password': '1234',
            'database': 'trivselsinitiativ',
            'port': 3306
        }

    def read_csv(self, path):
        
        result = []

        with open(path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)

            header = next(csv_reader)

            for line in csv_reader:
                result.append(line)
                
            
        return header, result

    def authenticate_user(self, id):
        mydb = self.connect_DB()
        mycursor = mydb.cursor()

        
        # Execute a query to check if the employee_id exists
        sql = f"SELECT * FROM employee WHERE person_id = {id}"
        mycursor.execute(sql)
        

        
        # Fetch the result
        result = mycursor.fetchone()

        # Check if the result is not None (i.e., the employee_id exists)
        if result:
            print(f"Employee with ID {id} exists.")
            return True
        else:
            print(f"Employee with ID {id} does not exist.")
            return False



    def csv_to_DB(self, path, data_dict):
        data = self.read_csv(path)
        header = data[0]
        data = data[1]
        
        #print(data)

        tables_list = list(data_dict.keys())


        header = list(map(str.lower,header))
        header = [string.replace(" ", "_") for string in header]


        header_str = ",".join(str(element) for element in header)  
  
        #print(header)
        #print(header.index('age'))


        data_list = []


        for item in data:
            data_dict = {
                'employee' : {
                    'person_id' : f"'{item[0]}'",
                    'gender': f"'{item[1]}'",
                    'age' : f"{item[2]}",
                    'occupation' : f"'{item[3]}'"
                },
                'activity' : {
                    'activity_level' : f"{item[6]}",
                    'daily_steps' : f"{item[11]}"
                },
                'sleep' : {
                    'sleep_duration' : f"{item[4]}",
                    'quality_of_sleep' : f"{item[5]}",
                    'sleep_disorder' : f"'{item[12]}'"
                },
                'health' : {
                    'stress_level' : f"{item[7]}",
                    'bmi_category' : f"'{item[8]}'",
                    'blood_pressure' : f"'{item[9]}'",
                    'heart_rate' : f"{item[10]}"
                }
            }  
            
            print(data_dict)
            self.write(data_dict)



        
        for column in header:
            for table, attributes in data_dict.items():
                if column in attributes:
                    #print(f"The column '{column}' is in the table '{table}'.")
                    #ql = f"INSERT INTO {table} ({columns_str}) VALUES ({values_str})"   


                    break


        for values in data:
            values_str = ",".join(str(element) for element in values)  

            #sql = f"INSERT INTO {table} ({columns_str}) VALUES ({values_str})"  


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


    def read(self, data_dict, select = (False, '', '', '')):
        tables_list = list(data_dict.keys())

        #select = (True, 'employee', 'occupation', 'Doctor')


        print(select[0])
        print(select[1])
        mydb = self.connect_DB()
        mycursor = mydb.cursor()


        data_list = []
        for table in tables_list:
            column_str = ", ".join(str(element) for element in data_dict[table])  

            if select[1] == table and select[0] == True:
                sql = f"SELECT {column_str} FROM {table} WHERE {select[2]} = '{select[3]}'" 
            else: 
                sql = f"SELECT {column_str} FROM {table}"
                

                #sql = f"IF EXISTS (SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'employee' AND COLUMN_NAME = 'occupation') SELECT {column_str} FROM {table} WHERE {select[0]} = {select[1]}; ELSE SELECT 'Column does not exist' AS result; END IF;"

            mycursor.execute(sql)

            desc = mycursor.description
            #print(desc)
            column_names = [col[0] for col in desc]
            #print("col:", column_names)
            data = [dict(zip(column_names, row))  
                    for row in mycursor.fetchall()]
            data_list.append(data)

            #print(data_list)
        self.close_DB(mydb)


        combined_data = []
        # Iterate over the lists and combine dictionaries with the same index
        for i in range(len(data_list[0])):
            combined_dict = {}
            for sublist in data_list:
                combined_dict.update(sublist[i])
            combined_data.append(combined_dict)

        # Print the result
        return combined_data



    def write(self, data_dict):
        mydb = self.connect_DB()
        
        mycursor = mydb.cursor()

        tables_list = list(data_dict.keys())
        print(tables_list)

        for table in tables_list:
            
            columns_list = list(data_dict[table].keys())
            columns_str = ",".join(str(element) for element in columns_list)

            values_list = columns_list = list(data_dict[table].values())
            values_str = ",".join(str(element) for element in values_list)

            
            if table == 'employee':
                sql = f"INSERT INTO {table} ({columns_str}) VALUES ({values_str})"  
                mycursor.execute(sql)
                employee_id = mycursor.lastrowid
            else:
                print(table)
                print(employee_id)
                columns_str += ',employee_Id'
                values_str += f',{employee_id}'
                print(columns_str)
                print(values_str)

                sql = f"INSERT INTO {table} ({columns_str}) VALUES ({values_str})"  
                mycursor.execute(sql)
            
            

        mydb.commit()

        self.close_DB(mydb)


    def delete(self, table, column ,id_list):
        id_str = ",".join(str(element) for element in id_list)
        print(id_str)

        mydb = self.connect_DB()
        mycursor = mydb.cursor()
        
        sql = f"DELETE FROM {table} WHERE {column} IN ({id_str})"

        print(sql)
        mycursor.execute(sql)
        mydb.commit()
        self.close_DB(mydb)


data_dict = {
    'employee' : {
        'person_id' : 1,
        'gender': "'female'",
        'age' : 54,
        'occupation' : "'Doctor'"
    },
    'activity' : {
        'activity_level' : 5,
        'daily_steps' : 10000
    },
    'sleep' : {
        'sleep_duration' : 7.6,
        'quality_of_sleep' : 5,
        'sleep_disorder' : "'asd'"
    },
    'health' : {
        'stress_level' : 6,
        'bmi_category' : "'Normal'",
        'blood_pressure' : "'125/80 '",
        'heart_rate' : 70
    }
}

if __name__ == "__main__":

    data_dict = {
        'employee' : ['person_id', 'gender', 'age', 'occupation'],
         'health' : ['stress_level', 'bmi_category', 'blood_pressure', 'heart_rate'],
         'activity' : ['activity_level', 'daily_steps'],
         'sleep' : ['sleep_duration', 'quality_of_sleep', 'sleep_disorder']
    }


    data = Data()
    #data.write(data_dict)
    data.read(data_dict)
    #data.csv_to_DB('G:/Mit drev/IBA/IT-Arkitektur/Project 3 - Eksamen/Projekt 3/Sleep_health_and_lifestyle_dataset.csv', data_dict)
    #data.read_by_colunm()