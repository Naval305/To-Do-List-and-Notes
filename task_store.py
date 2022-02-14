class GetData:
    def __init__(self, task, desc, time, date, priority):
        self.task = task
        self.desc = desc
        self.jump = ''
        self.date = date
        self.time = time
        self.priority = priority

    def get_data(self):
        with open('database_files\\tasks_db.txt', 'r') as data_file: 
            self.data_lines= data_file.readlines()
        with open('database_files\\tasks_db.txt', 'r') as file:
            self.content= file.read()
        self.store_data()

    # this method is responsible for storing the tasks data in the database file when they get added
    def store_data(self):
        self.descision=[]

        with open('database_files\\tasks_db.txt', 'a') as db1:
            
            if self.content == '':
                self.idd= '1'
            else:
                self.idd= str(int(self.data_lines[-1][3])+1)
            
            if len(self.data_lines) != 0:
                for line in self.data_lines:
                    line= str(line[5:].strip())
                    if line == f'{self.task};{self.desc};{self.time};{self.date};{self.priority}':
                        self.descision.append(1)
                    elif line != f'{self.task};{self.desc};{self.time};{self.date};{self.priority}':
                        pass
                if len(self.descision) == 0:   
                    db1.write(f'ID:{self.idd}>{self.task};{self.desc.strip()};{self.time};{self.date};{self.priority}\n')
                else:
                    pass
            if len(self.data_lines) == 0:
                db1.write(f'ID:{self.idd}>{self.task};{self.desc.strip()};{self.time};{self.date};{self.priority}\n')

    # this method is responsible for sending the tasks data to the cards generator when the app starts
    def send_data(self):
        with open('database_files\\tasks_db.txt', 'r') as file:
            self.data_lines= file.readlines()
            if len(self.data_lines) == 0:
                return 'database empty'
            else:
                self.data_lines = [line.strip() for line in self.data_lines]
                return self.data_lines

   # this method is responsible for deleting the task data from the database file:

    def delete_data(self, task, desc, time, date, priority):
        self.task = task
        self.desc = desc
        self.date = date
        self.time = time
        self.priority = priority
        self.victim = str(self.task) + ';' + str(self.desc) + ';' + str(self.time) + ';' + str(self.date) + ';' + str(self.priority)
        self.the_lines=[]

        with open('database_files\\tasks_db.txt', 'r') as file:
            self.list= file.readlines()
        for one in self.list:
            self.the_lines.append(one[5:].strip())

        for line in self.the_lines:
            if line == self.victim:
                self.the_lines.remove(line)
            elif line != self.victim:
                pass

        with open('database_files\\tasks_db.txt', 'w') as file_2:
            file_2.write('')

        with open('database_files\\tasks_db.txt', 'w+') as file_3:
            for num, the_line in enumerate(self.the_lines):
                file_3.write('ID:' + str(num+1) + '>' + the_line + '\n')