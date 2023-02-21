import sqlite3

class Data_base:

    def __init__(self, name = 'system.db') -> None:        
        self.name = name

    def connect(self):
        self.connection = sqlite3.connect(self.name)

    def close_connection(self):
        try:
            self.connection.close()
        except:
            pass
    
    def create_table(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS funcionarios(id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, matricula TEXT NOT NULL UNIQUE, setor TEXT, ano_2019 INTEGER, ano_2020 INTEGER, ano_2021 INTEGER, ano_2022 INTEGER, ano_2023 INTEGER);           
        """)
    
    def insert_table(self, fullDataSet):

        campos_tabela = ('nome','matricula','setor','ano_2019','ano_2020','ano_2021','ano_2022', 'ano_2023')

        qntd = ("?,?,?,?,?,?,?,?")
        cursor = self.connection.cursor()

        try:
            cursor.execute(f"""INSERT INTO funcionarios {campos_tabela}
            VALUES({qntd})""", fullDataSet)
            self.connection.commit()
            return("OK")

        except:
            return "Erro"

    def select_all(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT nome, matricula, setor, ano_2019, ano_2020, ano_2021, ano_2022, ano_2023 FROM funcionarios ORDER BY nome")
            funcionarios = cursor.fetchall()
            return funcionarios
        except:
            pass

    def pdf_19(self):
            try:
                cursor = self.connection.cursor()
                cursor.execute("SELECT nome, matricula, setor, ano_2019, ano_2020, ano_2021, ano_2022, ano_2023 FROM funcionarios WHERE ano_2019 < 30 ORDER BY nome")
                funcionarios = cursor.fetchall()
                return funcionarios
            except:
                pass
    
    def select_19(self):
            try:
                cursor = self.connection.cursor()
                cursor.execute("SELECT nome, matricula, ano_2019 FROM funcionarios WHERE ano_2019 < 30 ORDER BY nome")
                funcionarios = cursor.fetchall()
                return funcionarios
            except:
                pass
    
    def pdf_20(self):
            try:
                cursor = self.connection.cursor()
                cursor.execute("SELECT nome, matricula, setor, ano_2019, ano_2020, ano_2021, ano_2022, ano_2023 FROM funcionarios WHERE ano_2020 < 30 ORDER BY nome")
                funcionarios = cursor.fetchall()
                return funcionarios
            except:
                pass

    def select_20(self):
            try:
                cursor = self.connection.cursor()
                cursor.execute("SELECT nome, matricula, ano_2020 FROM funcionarios WHERE ano_2020 < 30 ORDER BY nome")
                funcionarios = cursor.fetchall()
                return funcionarios
            except:
                pass

    def pdf_21(self):
            try:
                cursor = self.connection.cursor()
                cursor.execute("SELECT nome, matricula, setor, ano_2019, ano_2020, ano_2021, ano_2022, ano_2023 FROM funcionarios WHERE ano_2021 < 30 ORDER BY nome")
                funcionarios = cursor.fetchall()
                return funcionarios
            except:
                pass
    
    def select_21(self):
            try:
                cursor = self.connection.cursor()
                cursor.execute("SELECT nome, matricula, ano_2021 FROM funcionarios WHERE ano_2021 < 30 ORDER BY nome")
                funcionarios = cursor.fetchall()
                return funcionarios
            except:
                pass
    
    def pdf_22(self):
            try:
                cursor = self.connection.cursor()
                cursor.execute("SELECT nome, matricula, setor, ano_2019, ano_2020, ano_2021, ano_2022, ano_2023 FROM funcionarios WHERE ano_2022 < 30 ORDER BY nome")
                funcionarios = cursor.fetchall()
                return funcionarios
            except:
                pass

    def select_22(self):
            try:
                cursor = self.connection.cursor()
                cursor.execute("SELECT nome, matricula, ano_2022 FROM funcionarios WHERE ano_2022 < 30 ORDER BY nome")
                funcionarios = cursor.fetchall()
                return funcionarios
            except:
                pass
    
    def pdf_23(self):
            try:
                cursor = self.connection.cursor()
                cursor.execute("SELECT nome, matricula, setor, ano_2019, ano_2020, ano_2021, ano_2022, ano_2023 FROM funcionarios WHERE ano_2023 < 30 ORDER BY nome")
                funcionarios = cursor.fetchall()
                return funcionarios
            except:
                pass

    def select_23(self):
            try:
                cursor = self.connection.cursor()
                cursor.execute("SELECT nome, matricula, ano_2023 FROM funcionarios WHERE ano_2023 < 30 ORDER BY nome")
                funcionarios = cursor.fetchall()
                return funcionarios
            except:
                pass

    def select_padrao19(self):
            try:
                cursor = self.connection.cursor()
                cursor.execute("SELECT setor FROM funcionarios WHERE ano_2019 <> '-' ORDER BY nome")
                funcionarios = cursor.fetchall()
                return funcionarios
            except:
                pass
    
    def select_padrao20(self):
            try:
                cursor = self.connection.cursor()
                cursor.execute("SELECT setor FROM funcionarios WHERE ano_2020 <> '-' ORDER BY nome")
                funcionarios = cursor.fetchall()
                return funcionarios
            except:
                pass
    
    def select_padrao21(self):
            try:
                cursor = self.connection.cursor()
                cursor.execute("SELECT setor FROM funcionarios WHERE ano_2021 <> '-' ORDER BY nome")
                funcionarios = cursor.fetchall()
                return funcionarios
            except:
                pass
    
    def select_padrao22(self):
            try:
                cursor = self.connection.cursor()
                cursor.execute("SELECT setor FROM funcionarios WHERE ano_2022 <> '-' ORDER BY nome")
                funcionarios = cursor.fetchall()
                return funcionarios
            except:
                pass

    def select_padrao23(self):
            try:
                cursor = self.connection.cursor()
                cursor.execute("SELECT setor FROM funcionarios WHERE ano_2023 <> '-' ORDER BY nome")
                funcionarios = cursor.fetchall()
                return funcionarios
            except:
                pass
   
    def delete(self, id):

        try:
            cursor = self.connection.cursor()
            cursor.execute(f"DELETE FROM funcionarios WHERE id= '{id}' ")

            self.connection.commit()

            return "Cadastro excluido"

        except:
            return "Erro"

    def update(self, fullDataSet):

        cursor = self.connection.cursor()
        cursor.execute(f""" UPDATE funcionarios set
            nome = '{fullDataSet[1]}',
            matricula = '{fullDataSet[2]}',
            setor = '{fullDataSet[3]}',
            2019 = '{fullDataSet[4]}',
            2020 = '{fullDataSet[5]}',
            2021 = '{fullDataSet[6]}',
            2022 = '{fullDataSet[7]}',
            2023 = '{fullDataSet[8]}',
            WHERE matricula = '{fullDataSet[0]}'""")

        self.connection.commit()

    def update_table(self, fullDataSet):
        
        campos_tabela = ('nome','matricula','setor','ano_2019','ano_2020','ano_2021','ano_2022', 'ano_2023')

        qntd = ("?,?,?,?,?,?,?,?")
        cursor = self.connection.cursor()

        try:
            cursor.execute(f"""INSERT INTO funcionarios {campos_tabela}
            VALUES({qntd})""", fullDataSet)
            self.connection.commit()
            return("OK")

        except:
            return "Erro"
