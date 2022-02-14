class GetNotes:
    def __init__(self, text, current_date_time):
        self.text = text
        self.current_date_time =current_date_time

    def getdata(self):
        with open('database_files\\notes_db.txt', 'r') as db0: 
            self.data_lines= db0.readlines()
        with open('database_files\\notes_db.txt', 'r') as db00:
            self.content= db00.read()
        self.storedata()

    def storedata(self):
        self.descision = []
        with open('database_files\\notes_db.txt', 'a') as db1:
            if self.content == '':
                self.idd = '1'
            else:
                self.idd = str(int(self.data_lines[-1][3])+1)
                
            if len(self.data_lines) != 0:
                for line in self.data_lines:
                    line= str(line[5:].strip())
                    if line == f'{self.text};{self.current_date_time}':
                        self.descision.append(1)
                    elif line != f'{self.text};{self.current_date_time}':
                        pass
                if len(self.descision) == 0:   
                    db1.write(f'ID:{self.idd}>{self.text};{self.current_date_time}\n')
                else:
                    pass
            if len(self.data_lines) == 0:
                db1.write(f'ID:{self.idd}>{self.text};{self.current_date_time}\n')

    def senddata(self):
        with open('database_files\\notes_db.txt', 'r') as db2:
            self.data_lines2= db2.readlines()
            if len(self.data_lines2) == 0:
                return 'databaase empty'
            else:
                self.data_lines2 = [line.strip() for line in self.data_lines2]
                return self.data_lines2

    def deletedata(self, text, current_date_time):
        self.text = text
        self.current_date_time = current_date_time
        self.victim = str(self.text) + ';' + str(self.current_date_time)
        self.the_lines = []
        
        with open('database_files\\notes_db.txt', 'r') as target:
            self.lista = target.readlines()
        for one in self.lista:
            self.the_lines.append(one[5:].strip())

        for line in self.the_lines:
            if line == self.victim:
                self.the_lines.remove(line)
            elif line != self.victim:
                pass

        with open('database_files\\notes_db.txt', 'w') as target1:
            target1.write('')

        with open('database_files\\notes_db.txt', 'w+') as target2:
            for num, the_line in enumerate(self.the_lines):
                target2.write('ID:' + str(num + 1) + '>' + the_line + '\n')