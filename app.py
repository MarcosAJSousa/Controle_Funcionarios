from tkinter import filedialog
from PyQt6 import uic, QtWidgets, QtCore
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QIntValidator
from reportlab.pdfgen.canvas import Canvas
from datetime import datetime
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.platypus import BaseDocTemplate, Frame, Paragraph, PageBreak, \
    PageTemplate, FrameBreak, NextPageTemplate
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from database import Data_base
import webbrowser
import pandas as pd
import sqlite3

id = 0
valor = 0

def Go_home():
    home.stackedWidget.setCurrentWidget(home.page)
    home.tableWidget.clearContents()
    home.buscar.setText('')
    home.filtro.setCurrentIndex(-1)

def Tela_Cadastro():
    home.stackedWidget.setCurrentWidget(home.page_2)
    home.Box_19.setPlaceholderText(" Situação:")
    home.Box_20.setPlaceholderText(" Situação:")
    home.Box_21.setPlaceholderText(" Situação:")
    home.Box_22.setPlaceholderText(" Situação:")
    home.Box_23.setPlaceholderText(" Situação:")

def Tela_Consulta():   
    home.stackedWidget.setCurrentWidget(home.page_3)
    home.filtro.setPlaceholderText(" Filtrar por:")
    home.stackedWidget_2.setCurrentWidget(home.page_10)
    home.stackedWidget_4.setCurrentWidget(home.page_16)

    home.tableWidget.setColumnWidth(0,500)
    home.tableWidget.setColumnWidth(1,150)
    home.tableWidget.setColumnWidth(2,300)
    home.tableWidget.setColumnWidth(3,80)
    home.tableWidget.setColumnWidth(4,80)
    home.tableWidget.setColumnWidth(5,80)
    home.tableWidget.setColumnWidth(6,80)
    home.tableWidget.setColumnWidth(7,80)
    home.tableWidget.setColumnWidth(8,80)

def Tela_Dashboard():
    home.stackedWidget.setCurrentWidget(home.page_8)
    home.stackedWidget_3.setCurrentWidget(home.page_11)
    
def Tela_Relatorios():
    home.stackedWidget.setCurrentWidget(home.page_9)

def index_changed(i):
    index = i
    
    if index == 1:
        home.buscar_2.setText('')
        home.stackedWidget_4.setCurrentWidget(home.page_15)
    else:
        home.buscar.setText('')
        home.stackedWidget_4.setCurrentWidget(home.page_14)
    pass

def Cadastrar(fullDataSet):
    try:
        db = Data_base()
        db.connect()

        input_nome = home.input_nome.text().upper()
        input_matricula = home.input_matricula.text()
        input_setor = home.input_setor.text().upper()

        inp19 = home.input_19.text()
        inp20 = home.input_20.text()
        inp21 = home.input_21.text()
        inp22 = home.input_22.text()
        inp23 = home.input_23.text()

        if home.input_nome.text() == "" or home.input_matricula.text() == "" or home.input_setor.text() == "" or home.input_19.text() == ""  or home.input_20.text() == "" or home.input_21.text() == "" or home.input_22.text() == "" or home.input_23.text() == "" :
            raise Exception(QMessageBox.warning(home, 'RH - CONSULTA', 'Verifique se todos os dados estão preenchidos corretamente!'))

        fullDataSet = ( str(input_nome),  str(input_matricula), str(input_setor), str(inp19), str(inp20), str(inp21), str(inp22), str(inp23))

        #CADASTRAR NO BANCO DE DADOS
        resp = db.insert_table(fullDataSet)

        if resp == "OK":
            QMessageBox.about(home, 'Mensagem', 'Cadastro realizado com sucesso!')
            db.close_connection()
            home.input_nome.setText('')
            home.input_matricula.setText('')
            home.input_setor.setText('')
            home.input_19.setText('')
            home.input_20.setText('')
            home.input_21.setText('')
            home.input_22.setText('')
            home.input_23.setText('')
            home.Box_19.setCurrentIndex(-1)
            home.Box_20.setCurrentIndex(-1)
            home.Box_21.setCurrentIndex(-1)
            home.Box_22.setCurrentIndex(-1)
            home.Box_23.setCurrentIndex(-1)
            return
        else:
            QMessageBox.warning(home, 'RH - CONSULTA', 'Atenção! Essa Matricula já foi cadastrada no sistema!')
            db.close_connection()
    except:
        pass

def Consulta_all():
    try:
        db = Data_base()
        db.connect()
        cursor = db.connection.cursor()
        cursor.execute("SELECT nome, matricula, setor, ano_2019, ano_2020, ano_2021, ano_2022, ano_2023 FROM funcionarios ORDER BY nome")
        dados_lidos = cursor.fetchall()
        home.tableWidget.setRowCount(len(dados_lidos))
        
        for i in range(0, len(dados_lidos)):
            for j in range (0,8):
                home.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
        home.stackedWidget_2.setCurrentWidget(home.page_4)
    except:
        QMessageBox.critical(home, 'RH - CONSULTA', 'Algo não saiu como planejado!')

def Consulta_filtro():
    if home.filtro.currentText() == " Nome":
        try:
            db = Data_base()
            db.connect()
            cursor = db.connection.cursor()
            sua_busca = home.buscar.text().upper()
            cursor.execute("SELECT nome, matricula, setor, ano_2019, ano_2020, ano_2021, ano_2022, ano_2023 FROM funcionarios WHERE nome LIKE '%{}%' ORDER BY nome ASC;".format(sua_busca) )
            dados = cursor.fetchall()
            
            home.tableWidget.setRowCount(len(dados))
            home.tableWidget.setColumnCount(8)
            for i in range(0, len(dados)):
                for j in range (0,8):
                    home.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados[i][j])))
                        
            if dados == []:
                QMessageBox.about(home, 'RH - CONSULTA', '   Não foi encontrado dados referente a sua pesquisa!\n  \n Verifique os dados de sua pesquisa e a caixa de seleção       ')
            home.stackedWidget_2.setCurrentWidget(home.page_5)
        except:
            QMessageBox.critical(home, 'RH - CONSULTA', 'Algo não saiu como planejado!')
    
    elif home.filtro.currentText() == " Matrícula":
        try:
            db = Data_base()
            db.connect()
            cursor = db.connection.cursor()
            sua_busca = home.buscar_2.text().upper()
            cursor.execute("SELECT nome, matricula, setor, ano_2019, ano_2020, ano_2021, ano_2022, ano_2023 FROM funcionarios WHERE matricula LIKE '%{}%' ORDER BY nome ASC;".format(sua_busca) )
            dados = cursor.fetchall()
            
            home.tableWidget.setRowCount(len(dados))
            home.tableWidget.setColumnCount(8)
            for i in range(0, len(dados)):
                for j in range (0,8):
                    home.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados[i][j])))
            
            if dados == []:
                QMessageBox.about(home, 'RH - CONSULTA', '   Não foi encontrado dados referente a sua pesquisa!\n  \n Verifique os dados de sua pesquisa e a caixa de seleção       ')
            
            home.stackedWidget_2.setCurrentWidget(home.page_6)
        except:
            QMessageBox.critical(home, 'RH - CONSULTA', 'Algo não saiu como planejado!')
    
    elif home.filtro.currentText() == " Setor":
        try:
            db = Data_base()
            db.connect()
            cursor = db.connection.cursor()
            sua_busca = home.buscar.text().upper()
            cursor.execute("SELECT nome, matricula, setor, ano_2019, ano_2020, ano_2021, ano_2022, ano_2023 FROM funcionarios WHERE setor LIKE '%{}%' ORDER BY nome ASC;".format(sua_busca) )
            dados = cursor.fetchall()
            
            home.tableWidget.setRowCount(len(dados))
            home.tableWidget.setColumnCount(8)
            for i in range(0, len(dados)):
                for j in range (0,8):
                    home.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados[i][j])))
            
            if dados == []:
                QMessageBox.about(home, 'RH - CONSULTA', '   Não foi encontrado dados referente a sua pesquisa!\n  \n Verifique os dados de sua pesquisa e a caixa de seleção       ')
            home.stackedWidget_2.setCurrentWidget(home.page_7)
        except:
            QMessageBox.critical(home, 'RH - CONSULTA', 'Algo não saiu como planejado!')
    
    else:
        QMessageBox.about(home, 'RH - CONSULTA', 'Selecione um filtro para fazer a pesquisa!')
        home.tableWidget.clearContents()

def show_all():
    try:
        global id
        db = Data_base()
        db.connect()
        cursor = db.connection.cursor()
        edicao.show()
        edicao.stackedWidget.setCurrentWidget(edicao.page)

        line = home.tableWidget.currentRow()
        cursor.execute('SELECT id FROM funcionarios ORDER BY nome')
        dados_lidos = cursor.fetchall()
        matricula = dados_lidos[line][0]
        cursor.execute("SELECT * FROM funcionarios WHERE id="+ str(matricula) )
        show_view = cursor.fetchall()
        
        id = matricula
        
        edicao.nome.setText(str(show_view[0][1]))
        edicao.matricula.setText(str(show_view[0][2]))
        edicao.setor.setText(str(show_view[0][3]))

        edicao.dias_19.setText(str(show_view[0][4]))
        edicao.dias_20.setText(str(show_view[0][5]))
        edicao.dias_21.setText(str(show_view[0][6]))
        edicao.dias_22.setText(str(show_view[0][7]))
        edicao.dias_23.setText(str(show_view[0][8]))
    except:
        QMessageBox.critical(home, 'RH - CONSULTA', 'Algo não saiu como planejado!')  
        edicao.close()
        
def atualiza_all():
    try:
        global id
        db = Data_base()
        db.connect()
        cursor = db.connection.cursor()

        nome = edicao.nome.text().upper()
        matricula = edicao.matricula.text()
        setor = edicao.setor.text().upper()

        ano_19 = edicao.dias_19.text()
        ano_20 = edicao.dias_20.text()
        ano_21 = edicao.dias_21.text()
        ano_22 = edicao.dias_22.text()
        ano_23 = edicao.dias_23.text()

        cursor.execute("UPDATE funcionarios SET nome = '{}', matricula = '{}', setor = '{}', ano_2019 = '{}', ano_2020 = '{}', ano_2021 = '{}', ano_2022 = '{}', ano_2023 = '{}' WHERE id = '{}' ".format(nome, matricula, setor, ano_19, ano_20, ano_21, ano_22, ano_23, id) )     
        db.connection.commit()
        db.close_connection()
        
        QMessageBox.about(home, 'RH - CONSULTA', 'Cadastro Atualizado com Sucesso!')
        
        
        edicao.close()
        Consulta_all()
         
    except:
        QMessageBox.critical(home, 'RH - CONSULTA', 'Algo não saiu como planejado!')

def show_nome():
    try:
        global id
        db = Data_base()
        db.connect()
        cursor = db.connection.cursor()
        edicao.show()
        edicao.stackedWidget.setCurrentWidget(edicao.page_3)
        sua_busca = home.buscar.text().upper()

        linha = home.tableWidget.currentRow()
        cursor.execute("SELECT id FROM funcionarios WHERE nome LIKE '%{}%' ORDER BY nome;".format(sua_busca))
        dados = cursor.fetchall()
        valor_id = dados[linha][0]
        cursor.execute('SELECT * FROM funcionarios WHERE id='+ str(valor_id))
        show_view = cursor.fetchall()

        id = valor_id

        edicao.nome.setText(str(show_view[0][1]))
        edicao.matricula.setText(str(show_view[0][2]))
        edicao.setor.setText(str(show_view[0][3]))

        edicao.dias_19.setText(str(show_view[0][4]))
        edicao.dias_20.setText(str(show_view[0][5]))
        edicao.dias_21.setText(str(show_view[0][6]))
        edicao.dias_22.setText(str(show_view[0][7]))
        edicao.dias_23.setText(str(show_view[0][8]))
    except:    
        QMessageBox.critical(home, 'RH - CONSULTA', 'Algo não saiu como planejado!')
        edicao.close()

def show_matricula():
    try:
        global id
        db = Data_base()
        db.connect()
        cursor = db.connection.cursor()
        edicao.show()
        edicao.stackedWidget.setCurrentWidget(edicao.page_2)
        sua_busca = home.buscar_2.text()

        linha = home.tableWidget.currentRow()
        cursor.execute("SELECT id FROM funcionarios WHERE matricula LIKE '%{}%' ORDER BY nome;".format(sua_busca))
        dados = cursor.fetchall()
        valor_id = dados[linha][0]
        cursor.execute('SELECT * FROM funcionarios WHERE id='+ str(valor_id))
        show_view = cursor.fetchall()

        id = valor_id

        edicao.nome.setText(str(show_view[0][1]))
        edicao.matricula.setText(str(show_view[0][2]))
        edicao.setor.setText(str(show_view[0][3]))

        edicao.dias_19.setText(str(show_view[0][4]))
        edicao.dias_20.setText(str(show_view[0][5]))
        edicao.dias_21.setText(str(show_view[0][6]))
        edicao.dias_22.setText(str(show_view[0][7]))
        edicao.dias_23.setText(str(show_view[0][8]))        
    except:    
        QMessageBox.critical(home, 'RH - CONSULTA', 'Algo não saiu como planejado!')
        edicao.close()

def show_setor():
    try:
        global id
        db = Data_base()
        db.connect()
        cursor = db.connection.cursor()
        edicao.show()
        edicao.stackedWidget.setCurrentWidget(edicao.page_4)
        sua_busca = home.buscar.text().upper()

        linha = home.tableWidget.currentRow()
        cursor.execute("SELECT id FROM funcionarios WHERE setor LIKE '%{}%' ORDER BY nome;".format(sua_busca))
        dados = cursor.fetchall()
        valor_id = dados[linha][0]
        cursor.execute('SELECT * FROM funcionarios WHERE id='+ str(valor_id))
        show_view = cursor.fetchall()

        id = valor_id

        edicao.nome.setText(str(show_view[0][1]))
        edicao.matricula.setText(str(show_view[0][2]))
        edicao.setor.setText(str(show_view[0][3]))

        edicao.dias_19.setText(str(show_view[0][4]))
        edicao.dias_20.setText(str(show_view[0][5]))
        edicao.dias_21.setText(str(show_view[0][6]))
        edicao.dias_22.setText(str(show_view[0][7]))
        edicao.dias_23.setText(str(show_view[0][8]))        
    except:    
        QMessageBox.critical(home, 'RH - CONSULTA', 'Algo não saiu como planejado!')
        edicao.close()

def selacao_1():
    if home.Box_19.currentText() == " (30) Férias Realizada":
        home.input_19.setText("30")

    elif home.Box_19.currentText() == " (15) Férias Pendente":
        home.input_19.setText("15")
       
    elif home.Box_19.currentText() == " (0) Férias a Realizar":
        home.input_19.setText("0")
        
    elif home.Box_19.currentText() == " (-) Não Consta":
        home.input_19.setText("-")
        
    else:
        home.input_19.setText("")

def selacao_2():
    
    if home.Box_20.currentText() == " (30) Férias Realizada":
        home.input_20.setText("30")

    elif home.Box_20.currentText() == " (15) Férias Pendente":
        home.input_20.setText("15")
       
    elif home.Box_20.currentText() == " (0) Férias a Realizar":
        home.input_20.setText("0")

    elif home.Box_20.currentText() == " (-) Não Consta":
        home.input_20.setText("-")

    else:
        home.input_20.setText("")

def selacao_3():
    
    if home.Box_21.currentText() == " (30) Férias Realizada":
        home.input_21.setText("30")

    elif home.Box_21.currentText() == " (15) Férias Pendente":
        home.input_21.setText("15")
       
    elif home.Box_21.currentText() == " (0) Férias a Realizar":
        home.input_21.setText("0")
    
    elif home.Box_21.currentText() == " (-) Não Consta":
        home.input_21.setText("-")

    else:
        home.input_21.setText("")

def selacao_4():
    
    if home.Box_22.currentText() == " (30) Férias Realizada":
        home.input_22.setText("30")

    elif home.Box_22.currentText() == " (15) Férias Pendente":
        home.input_22.setText("15")
       
    elif home.Box_22.currentText() == " (0) Férias a Realizar":
        home.input_22.setText("0")
    
    elif home.Box_22.currentText() == " (-) Não Consta":
        home.input_22.setText("-")

    else:
        home.input_22.setText("")

def selacao_5():
    
    if home.Box_23.currentText() == " (30) Férias Realizada":
        home.input_23.setText("30")

    elif home.Box_23.currentText() == " (15) Férias Pendente":
        home.input_23.setText("15")
       
    elif home.Box_23.currentText() == " (0) Férias a Realizar":
        home.input_23.setText("0")
    
    elif home.Box_23.currentText() == " (-) Não Consta":
        home.input_23.setText("-")

    else:
        home.input_23.setText("")

def edicao_1():
    if edicao.dias_19.text() == "30":
        edicao.comboBox.setCurrentIndex(0)
        edicao.dias_19.setText("")
    elif edicao.dias_19.text() == "15":
        edicao.comboBox.setCurrentIndex(1)
        edicao.dias_19.setText("")       
    elif edicao.dias_19.text() == "0":
        edicao.comboBox.setCurrentIndex(2)
        edicao.dias_19.setText("")        
    elif edicao.dias_19.text() == "-":
        edicao.comboBox.setCurrentIndex(3)
        edicao.dias_19.setText("")   
    else:
        edicao.dias_19.setText("")

def edicao_2():
    if edicao.dias_20.text() == "30":
        edicao.comboBox_2.setCurrentIndex(0)

    elif edicao.dias_20.text() == "15":
        edicao.comboBox_2.setCurrentIndex(1)
       
    elif edicao.dias_20.text() == "0":
        edicao.comboBox_2.setCurrentIndex(2)
        
    elif edicao.dias_20.text() == "-":
        edicao.comboBox_2.setCurrentIndex(3)   
    else:
        edicao.dias_20.setText("")

def edicao_3():
    if edicao.dias_21.text() == "30":
        edicao.comboBox_3.setCurrentIndex(0)

    elif edicao.dias_21.text() == "15":
        edicao.comboBox_3.setCurrentIndex(1)
       
    elif edicao.dias_21.text() == "0":
        edicao.comboBox_3.setCurrentIndex(2)
        
    elif edicao.dias_21.text() == "-":
        edicao.comboBox_3.setCurrentIndex(3)   
    else:
        edicao.dias_21.setText("")

def edicao_4():
    if edicao.dias_22.text() == "30":
        edicao.comboBox_4.setCurrentIndex(0)

    elif edicao.dias_22.text() == "15":
        edicao.comboBox_4.setCurrentIndex(1)
       
    elif edicao.dias_22.text() == "0":
        edicao.comboBox_4.setCurrentIndex(2)
        
    elif edicao.dias_22.text() == "-":
        edicao.comboBox_4.setCurrentIndex(3)   
    else:
        edicao.dias_22.setText("")

def edicao_5():
    if edicao.dias_23.text() == "30":
        edicao.comboBox_5.setCurrentIndex(0)

    elif edicao.dias_23.text() == "15":
        edicao.comboBox_5.setCurrentIndex(1)
       
    elif edicao.dias_23.text() == "0":
        edicao.comboBox_5.setCurrentIndex(2)
        
    elif edicao.dias_23.text() == "-":
        edicao.comboBox_5.setCurrentIndex(3)   
    else:
        edicao.dias_23.setText("")

def atualizacao_1():
    if  edicao.comboBox.currentText() == " (30) Férias Realizada":
        edicao.dias_19.setText("30")

    elif edicao.comboBox.currentText() == " (15) Férias Pendente":
        edicao.dias_19.setText("15") 
       
    elif edicao.comboBox.currentText() == " (0) Férias a Realizar":
        edicao.dias_19.setText("0") 
        
    elif edicao.comboBox.currentText() == " (-) Não Consta":
        edicao.dias_19.setText("-")    
    else:
        edicao.dias_19.setText("")

def atualizacao_2():
    if  edicao.comboBox_2.currentText() == " (30) Férias Realizada":
        edicao.dias_20.setText("30")  

    elif edicao.comboBox_2.currentText() == " (15) Férias Pendente":
        edicao.dias_20.setText("15")  
       
    elif edicao.comboBox_2.currentText() == " (0) Férias a Realizar":
        edicao.dias_20.setText("0") 
        
    elif edicao.comboBox_2.currentText() == " (-) Não Consta":
        edicao.dias_20.setText("-")     
    else:
        edicao.dias_20.setText("")

def atualizacao_3():
    if  edicao.comboBox_3.currentText() == " (30) Férias Realizada":
        edicao.dias_21.setText("30")

    elif edicao.comboBox_3.currentText() == " (15) Férias Pendente":
        edicao.dias_21.setText("15")  
       
    elif edicao.comboBox_3.currentText() == " (0) Férias a Realizar":
        edicao.dias_21.setText("0")  
        
    elif edicao.comboBox_3.currentText() == " (-) Não Consta":
        edicao.dias_21.setText("-")     
    else:
        edicao.dias_21.setText("")

def atualizacao_4():
    if  edicao.comboBox_4.currentText() == " (30) Férias Realizada":
        edicao.dias_22.setText("30")  

    elif edicao.comboBox_4.currentText() == " (15) Férias Pendente":
        edicao.dias_22.setText("15")  
       
    elif edicao.comboBox_4.currentText() == " (0) Férias a Realizar":
        edicao.dias_22.setText("0")  
        
    elif edicao.comboBox_4.currentText() == " (-) Não Consta":
        edicao.dias_22.setText("-")     
    else:
        edicao.dias_22.setText("")

def atualizacao_5():
    if  edicao.comboBox_5.currentText() == " (30) Férias Realizada":
        edicao.dias_23.setText("30")  

    elif edicao.comboBox_5.currentText() == " (15) Férias Pendente":
        edicao.dias_23.setText("15")  
       
    elif edicao.comboBox_5.currentText() == " (0) Férias a Realizar":
        edicao.dias_23.setText("0")  
        
    elif edicao.comboBox_5.currentText() == " (-) Não Consta":
        edicao.dias_23.setText("-")     
    else:
        edicao.dias_23.setText("")

def backup():
    try:
        file_name = 'backup.pdf'
        document_title = 'SECRETARIA DA MULHER - SEMU'
        title = 'LISTA DE SERVIDORES DA SECRETARIA DA MULHER'
        subtitle = 'RECURSOS HUMANOS - GESTÃO DE FÉRIAS'
        day = datetime.now().strftime("%d/%m/%Y")
        fecha_actual = f'DATA DE EMISSÃO: {day}'
        
        canvas = Canvas(file_name, pagesize=A4)
        
        doc = BaseDocTemplate(file_name)
        contents =[]
        width,height = A4
        
        frame_later = Frame(
            0.2*inch,
            0.6*inch,
            (width-0.5*inch)+0.17*inch,
            height-1*inch,
            leftPadding = 0,
            topPadding=0,
            id='col'
            )
        
        frame_table= Frame(
            0.2*inch,
            0.7*inch,
            (width-0.5*inch)+0.17*inch,
            height-2*inch,
            leftPadding = 0,
            topPadding=0,
            id='col'
            )


        laterpages = PageTemplate(id='laterpages',frames=[frame_later], pagesize=A4)
        firstpage = PageTemplate(id='firstpage',frames=[ frame_later, frame_table],pagesize=A4,)

        styleSheet = getSampleStyleSheet()
        style_title = styleSheet['Heading1']
        style_title.fontSize = 14
        style_title.fontName = 'Helvetica-Bold'
        style_title.alignment=TA_CENTER
        
        style_data = styleSheet['Normal']
        style_data.fontSize = 26
        style_data.fontName = 'Helvetica'
        style_data.alignment=TA_CENTER
        
        style_date = styleSheet['Normal']
        style_date.fontSize = 12
        style_date.fontName = 'Helvetica'
        style_date.alignment=TA_CENTER
        
        canvas.setTitle(document_title)
        
        contents.append(Paragraph(title, style_title))
        contents.append(Paragraph(subtitle, style_data))
        contents.append(Paragraph(fecha_actual, style_date))
        contents.append(FrameBreak())
        
        db = Data_base()
        db.connect()
        result = db.select_all()

        column1Heading = "NOME"
        column2Heading = "MATRICULA"
        column3Heading = "SETOR"
        column4Heading = "2019"
        column5Heading = "2020"
        column6Heading = "2021"
        column7Heading = "2022"
        column8Heading = "2023"

        data = [(column1Heading,column2Heading,column3Heading,column4Heading,column5Heading,column6Heading,column7Heading,column8Heading)]
        for i in range(0, len(result)):
            data.append([Paragraph(result[i][0]),Paragraph(result[i][1]),Paragraph(result[i][2]),str(result[i][3]),str(result[i][4]),str(result[i][5]),str(result[i][6]),str(result[i][7])],)
                
        tableThatSplitsOverPages = Table(data, colWidths=(3.2*inch, None, 1.6*inch, None, None, None, None, None))
        tableThatSplitsOverPages.hAlign = 'CENTER'
        tblStyle = TableStyle([('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                            ('VALIGN',(0,0),(-1,-1),'TOP'),
                            ('LINEBELOW',(0,0),(-1,-1),1,colors.black),
                            ('GRID',(0,0),(-1,-1),1,colors.black)])
        tblStyle.add('BACKGROUND',(0,0),(7,0),colors.lightblue)
        tblStyle.add('BACKGROUND',(0,1),(-1,-1),colors.white)
        tableThatSplitsOverPages.setStyle(tblStyle)
        contents.append(tableThatSplitsOverPages)   
        contents.append(NextPageTemplate('laterpages'))
        
        contents.append(PageBreak())

        doc.addPageTemplates([firstpage,laterpages])
        doc.build(contents)
        db.close_connection()
    except:
        QMessageBox.critical(home, 'RH - CONSULTA', 'Algo não saiu como planejado!')

def pdf_all():
    try:
        webbrowser.open("Relatório.pdf")
        file_name = 'Relatório.pdf'
        document_title = 'SECRETARIA DA MULHER - SEMU'
        title = 'LISTA DE SERVIDORES DA SECRETARIA DA MULHER'
        subtitle = 'RECURSOS HUMANOS - GESTÃO DE FÉRIAS'
        day = datetime.now().strftime("%d/%m/%Y")
        fecha_actual = f'DATA DE EMISSÃO: {day}'
        
        canvas = Canvas(file_name, pagesize=A4)
        
        doc = BaseDocTemplate(file_name)
        contents =[]
        width,height = A4
        
        frame_later = Frame(
            0.2*inch,
            0.6*inch,
            (width-0.5*inch)+0.17*inch,
            height-1*inch,
            leftPadding = 0,
            topPadding=0,
            id='col'
            )
        
        frame_table= Frame(
            0.2*inch,
            0.7*inch,
            (width-0.5*inch)+0.17*inch,
            height-2*inch,
            leftPadding = 0,
            topPadding=0,
            id='col'
            )


        laterpages = PageTemplate(id='laterpages',frames=[frame_later], pagesize=A4)
        firstpage = PageTemplate(id='firstpage',frames=[ frame_later, frame_table],pagesize=A4,)

        styleSheet = getSampleStyleSheet()
        style_title = styleSheet['Heading1']
        style_title.fontSize = 14
        style_title.fontName = 'Helvetica-Bold'
        style_title.alignment=TA_CENTER
        
        style_data = styleSheet['Normal']
        style_data.fontSize = 26
        style_data.fontName = 'Helvetica'
        style_data.alignment=TA_CENTER
        
        style_date = styleSheet['Normal']
        style_date.fontSize = 12
        style_date.fontName = 'Helvetica'
        style_date.alignment=TA_CENTER
        
        canvas.setTitle(document_title)
        
        contents.append(Paragraph(title, style_title))
        contents.append(Paragraph(subtitle, style_data))
        contents.append(Paragraph(fecha_actual, style_date))
        contents.append(FrameBreak())
        
        db = Data_base()
        db.connect()
        result = db.select_all()

        column1Heading = "NOME"
        column2Heading = "MATRÍCULA"
        column3Heading = "SETOR"
        column4Heading = "2019"
        column5Heading = "2020"
        column6Heading = "2021"
        column7Heading = "2022"
        column8Heading = "2023"

        data = [(column1Heading,column2Heading,column3Heading,column4Heading,column5Heading,column6Heading,column7Heading,column8Heading)]
        for i in range(0, len(result)):
            data.append([Paragraph(result[i][0]),Paragraph(result[i][1]),Paragraph(result[i][2]),str(result[i][3]),str(result[i][4]),str(result[i][5]),str(result[i][6]),str(result[i][7])],)
                
        tableThatSplitsOverPages = Table(data, colWidths=(3.2*inch, None, 1.6*inch, None, None, None, None, None))
        tableThatSplitsOverPages.hAlign = 'CENTER'
        tblStyle = TableStyle([('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                            ('VALIGN',(0,0),(-1,-1),'TOP'),
                            ('LINEBELOW',(0,0),(-1,-1),1,colors.black),
                            ('GRID',(0,0),(-1,-1),1,colors.black)])
        tblStyle.add('BACKGROUND',(0,0),(7,0),colors.lightblue)
        tblStyle.add('BACKGROUND',(0,1),(-1,-1),colors.white)
        tableThatSplitsOverPages.setStyle(tblStyle)
        contents.append(tableThatSplitsOverPages)   
        contents.append(NextPageTemplate('laterpages'))
        
        contents.append(PageBreak())

        doc.addPageTemplates([firstpage,laterpages])
        doc.build(contents)
        db.close_connection()
    except:
        QMessageBox.critical(home, 'RH - CONSULTA', 'Algo não saiu como planejado!')

def pdf_nome():
    try:
        webbrowser.open("Relatório.pdf")
        file_name = 'Relatório.pdf'
        document_title = 'SECRETARIA DA MULHER - SEMU'
        title = 'LISTA DE SERVIDORES DA SECRETARIA DA MULHER'
        subtitle = 'RECURSOS HUMANOS - GESTÃO DE FÉRIAS'
        day = datetime.now().strftime("%d/%m/%Y")
        fecha_actual = f'DATA DE EMISSÃO: {day}'
        
        canvas = Canvas(file_name, pagesize=A4)
        
        doc = BaseDocTemplate(file_name)
        contents =[]
        width,height = A4
        
        frame_later = Frame(
            0.2*inch,
            0.6*inch,
            (width-0.6*inch)+0.17*inch,
            height-1*inch,
            leftPadding = 0,
            topPadding=0,
            id='col'
            )
        
        frame_table= Frame(
            0.2*inch,
            0.7*inch,
            (width-0.5*inch)+0.17*inch,
            height-2*inch,
            leftPadding = 0,
            topPadding=0,
            id='col'
            )


        laterpages = PageTemplate(id='laterpages',frames=[frame_later], pagesize=A4)
        firstpage = PageTemplate(id='firstpage',frames=[ frame_later, frame_table],pagesize=A4,)

        styleSheet = getSampleStyleSheet()
        style_title = styleSheet['Heading1']
        style_title.fontSize = 14
        style_title.fontName = 'Helvetica-Bold'
        style_title.alignment=TA_CENTER
        
        style_data = styleSheet['Normal']
        style_data.fontSize = 26
        style_data.fontName = 'Helvetica'
        style_data.alignment=TA_CENTER
        
        style_date = styleSheet['Normal']
        style_date.fontSize = 12
        style_date.fontName = 'Helvetica'
        style_date.alignment=TA_CENTER
        
        canvas.setTitle(document_title)
        
        contents.append(Paragraph(title, style_title))
        contents.append(Paragraph(subtitle, style_data))
        contents.append(Paragraph(fecha_actual, style_date))
        contents.append(FrameBreak())
        
        db = Data_base()
        db.connect()
        cursor = db.connection.cursor()
        sua_busca = home.buscar.text().upper()
        cursor.execute("SELECT nome, matricula, setor, ano_2019, ano_2020, ano_2021, ano_2022, ano_2023 FROM funcionarios WHERE nome LIKE '%{}%' ORDER BY nome ASC;".format(sua_busca) )
        result = cursor.fetchall()

        column1Heading = "NOME"
        column2Heading = "MATRÍCULA"
        column3Heading = "SETOR"
        column4Heading = "2019"
        column5Heading = "2020"
        column6Heading = "2021"
        column7Heading = "2022"
        column8Heading = "2023"

        data = [(column1Heading,column2Heading,column3Heading,column4Heading,column5Heading,column6Heading,column7Heading,column8Heading)]
        for i in range(0, len(result)):
            data.append([Paragraph(result[i][0]),Paragraph(result[i][1]),Paragraph(result[i][2]),str(result[i][3]),str(result[i][4]),str(result[i][5]),str(result[i][6]),str(result[i][7])],)
                
        tableThatSplitsOverPages = Table(data, colWidths=(3.2*inch, None, 1.6*inch, None, None, None, None, None))
        tableThatSplitsOverPages.hAlign = 'CENTER'
        tblStyle = TableStyle([('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                            ('VALIGN',(0,0),(-1,-1),'TOP'),
                            ('LINEBELOW',(0,0),(-1,-1),1,colors.black),
                            ('GRID',(0,0),(-1,-1),1,colors.black)])
        tblStyle.add('BACKGROUND',(0,0),(7,0),colors.lightblue)
        tblStyle.add('BACKGROUND',(0,1),(-1,-1),colors.white)
        tableThatSplitsOverPages.setStyle(tblStyle)
        contents.append(tableThatSplitsOverPages)   
        #contents.append(elements)
        contents.append(NextPageTemplate('laterpages'))

        contents.append(PageBreak())

        doc.addPageTemplates([firstpage,laterpages])
        doc.build(contents)
        db.close_connection()
        
    except:
        QMessageBox.critical(home, 'RH - CONSULTA', 'Algo não saiu como planejado!')
    
def pdf_matricula():
    try:
        webbrowser.open("Relatório.pdf")
        file_name = 'Relatório.pdf'
        document_title = 'SECRETARIA DA MULHER - SEMU'
        title = 'LISTA DE SERVIDORES DA SECRETARIA DA MULHER'
        subtitle = 'RECURSOS HUMANOS - GESTÃO DE FÉRIAS'
        day = datetime.now().strftime("%d/%m/%Y")
        fecha_actual = f'DATA DE EMISSÃO: {day}'
        
        canvas = Canvas(file_name, pagesize=A4)
        
        doc = BaseDocTemplate(file_name)
        contents =[]
        width,height = A4
        
        frame_later = Frame(
            0.2*inch,
            0.6*inch,
            (width-0.6*inch)+0.17*inch,
            height-1*inch,
            leftPadding = 0,
            topPadding=0,
            id='col'
            )
        
        frame_table= Frame(
            0.2*inch,
            0.7*inch,
            (width-0.5*inch)+0.17*inch,
            height-2*inch,
            leftPadding = 0,
            topPadding=0,
            id='col'
            )


        laterpages = PageTemplate(id='laterpages',frames=[frame_later], pagesize=A4)
        firstpage = PageTemplate(id='firstpage',frames=[ frame_later, frame_table],pagesize=A4,)

        styleSheet = getSampleStyleSheet()
        style_title = styleSheet['Heading1']
        style_title.fontSize = 14
        style_title.fontName = 'Helvetica-Bold'
        style_title.alignment=TA_CENTER
        
        style_data = styleSheet['Normal']
        style_data.fontSize = 26
        style_data.fontName = 'Helvetica'
        style_data.alignment=TA_CENTER
        
        style_date = styleSheet['Normal']
        style_date.fontSize = 12
        style_date.fontName = 'Helvetica'
        style_date.alignment=TA_CENTER
        
        canvas.setTitle(document_title)
        
        contents.append(Paragraph(title, style_title))
        contents.append(Paragraph(subtitle, style_data))
        contents.append(Paragraph(fecha_actual, style_date))
        contents.append(FrameBreak())
        
        db = Data_base()
        db.connect()
        cursor = db.connection.cursor()
        sua_busca = home.buscar_2.text().upper()
        cursor.execute("SELECT nome, matricula, setor, ano_2019, ano_2020, ano_2021, ano_2022, ano_2023 FROM funcionarios WHERE matricula LIKE '%{}%' ORDER BY nome ASC;".format(sua_busca) )
        result = cursor.fetchall()

        column1Heading = "NOME"
        column2Heading = "MATRÍCULA"
        column3Heading = "SETOR"
        column4Heading = "2019"
        column5Heading = "2020"
        column6Heading = "2021"
        column7Heading = "2022"
        column8Heading = "2023"

        data = [(column1Heading,column2Heading,column3Heading,column4Heading,column5Heading,column6Heading,column7Heading,column8Heading)]
        for i in range(0, len(result)):
            data.append([Paragraph(result[i][0]),Paragraph(result[i][1]),Paragraph(result[i][2]),str(result[i][3]),str(result[i][4]),str(result[i][5]),str(result[i][6]),str(result[i][7])],)
                
        tableThatSplitsOverPages = Table(data, colWidths=(3.2*inch, None, 1.6*inch, None, None, None, None, None))
        tableThatSplitsOverPages.hAlign = 'CENTER'
        tblStyle = TableStyle([('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                            ('VALIGN',(0,0),(-1,-1),'TOP'),
                            ('LINEBELOW',(0,0),(-1,-1),1,colors.black),
                            ('GRID',(0,0),(-1,-1),1,colors.black)])
        tblStyle.add('BACKGROUND',(0,0),(7,0),colors.lightblue)
        tblStyle.add('BACKGROUND',(0,1),(-1,-1),colors.white)
        tableThatSplitsOverPages.setStyle(tblStyle)
        contents.append(tableThatSplitsOverPages)   
        #contents.append(elements)
        contents.append(NextPageTemplate('laterpages'))

        contents.append(PageBreak())

        doc.addPageTemplates([firstpage,laterpages])
        doc.build(contents)
        db.close_connection()
    except:
        QMessageBox.critical(home, 'RH - CONSULTA', 'Algo não saiu como planejado!')
    
def pdf_setor():
    try:
        webbrowser.open("Relatório.pdf")
        file_name = 'Relatório.pdf'
        document_title = 'SECRETARIA DA MULHER - SEMU'
        title = 'LISTA DE SERVIDORES DA SECRETARIA DA MULHER'
        subtitle = 'RECURSOS HUMANOS - GESTÃO DE FÉRIAS'
        day = datetime.now().strftime("%d/%m/%Y")
        fecha_actual = f'DATA DE EMISSÃO: {day}'
        
        canvas = Canvas(file_name, pagesize=A4)
        
        doc = BaseDocTemplate(file_name)
        contents =[]
        width,height = A4
        
        frame_later = Frame(
            0.2*inch,
            0.6*inch,
            (width-0.6*inch)+0.17*inch,
            height-1*inch,
            leftPadding = 0,
            topPadding=0,
            id='col'
            )
        
        frame_table= Frame(
            0.2*inch,
            0.7*inch,
            (width-0.5*inch)+0.17*inch,
            height-2*inch,
            leftPadding = 0,
            topPadding=0,
            id='col'
            )


        laterpages = PageTemplate(id='laterpages',frames=[frame_later], pagesize=A4)
        firstpage = PageTemplate(id='firstpage',frames=[ frame_later, frame_table],pagesize=A4,)

        styleSheet = getSampleStyleSheet()
        style_title = styleSheet['Heading1']
        style_title.fontSize = 14
        style_title.fontName = 'Helvetica-Bold'
        style_title.alignment=TA_CENTER
        
        style_data = styleSheet['Normal']
        style_data.fontSize = 26
        style_data.fontName = 'Helvetica'
        style_data.alignment=TA_CENTER
        
        style_date = styleSheet['Normal']
        style_date.fontSize = 12
        style_date.fontName = 'Helvetica'
        style_date.alignment=TA_CENTER
        
        canvas.setTitle(document_title)
        
        contents.append(Paragraph(title, style_title))
        contents.append(Paragraph(subtitle, style_data))
        contents.append(Paragraph(fecha_actual, style_date))
        contents.append(FrameBreak())
        
        db = Data_base()
        db.connect()
        cursor = db.connection.cursor()
        sua_busca = home.buscar.text().upper()
        cursor.execute("SELECT nome, matricula, setor, ano_2019, ano_2020, ano_2021, ano_2022, ano_2023 FROM funcionarios WHERE setor LIKE '%{}%' ORDER BY nome ASC;".format(sua_busca) )
        result = cursor.fetchall()

        column1Heading = "NOME"
        column2Heading = "MATRÍCULA"
        column3Heading = "SETOR"
        column4Heading = "2019"
        column5Heading = "2020"
        column6Heading = "2021"
        column7Heading = "2022"
        column8Heading = "2023"

        data = [(column1Heading,column2Heading,column3Heading,column4Heading,column5Heading,column6Heading,column7Heading,column8Heading)]
        for i in range(0, len(result)):
            data.append([Paragraph(result[i][0]),Paragraph(result[i][1]),Paragraph(result[i][2]),str(result[i][3]),str(result[i][4]),str(result[i][5]),str(result[i][6]),str(result[i][7])],)
                
        tableThatSplitsOverPages = Table(data, colWidths=(3.2*inch, None, 1.6*inch, None, None, None, None, None))
        tableThatSplitsOverPages.hAlign = 'CENTER'
        tblStyle = TableStyle([('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                            ('VALIGN',(0,0),(-1,-1),'TOP'),
                            ('LINEBELOW',(0,0),(-1,-1),1,colors.black),
                            ('GRID',(0,0),(-1,-1),1,colors.black)])
        tblStyle.add('BACKGROUND',(0,0),(7,0),colors.lightblue)
        tblStyle.add('BACKGROUND',(0,1),(-1,-1),colors.white)
        tableThatSplitsOverPages.setStyle(tblStyle)
        contents.append(tableThatSplitsOverPages)   
        #contents.append(elements)
        contents.append(NextPageTemplate('laterpages'))

        contents.append(PageBreak())

        doc.addPageTemplates([firstpage,laterpages])
        doc.build(contents)
        db.close_connection()
    except:
        QMessageBox.critical(home, 'RH - CONSULTA', 'Algo não saiu como planejado!')

def pdf_19():
    try:
        webbrowser.open("Relatório.pdf")
        file_name = 'Relatório.pdf'
        document_title = 'SECRETARIA DA MULHER - SEMU'
        title = 'LISTA DE SERVIDORES DA SECRETARIA DA MULHER'
        subtitle = 'RECURSOS HUMANOS - GESTÃO DE FÉRIAS'
        day = datetime.now().strftime("%d/%m/%Y")
        fecha_actual = f'DATA DE EMISSÃO: {day}'
        
        canvas = Canvas(file_name, pagesize=A4)
        
        doc = BaseDocTemplate(file_name)
        contents =[]
        width,height = A4
        
        frame_later = Frame(
            0.2*inch,
            0.6*inch,
            (width-0.6*inch)+0.17*inch,
            height-1*inch,
            leftPadding = 0,
            topPadding=0,
            id='col'
            )
        
        frame_table= Frame(
            0.2*inch,
            0.7*inch,
            (width-0.5*inch)+0.17*inch,
            height-2*inch,
            leftPadding = 0,
            topPadding=0,
            id='col'
            )


        laterpages = PageTemplate(id='laterpages',frames=[frame_later], pagesize=A4)
        firstpage = PageTemplate(id='firstpage',frames=[ frame_later, frame_table],pagesize=A4,)

        styleSheet = getSampleStyleSheet()
        style_title = styleSheet['Heading1']
        style_title.fontSize = 14
        style_title.fontName = 'Helvetica-Bold'
        style_title.alignment=TA_CENTER
        
        style_data = styleSheet['Normal']
        style_data.fontSize = 26
        style_data.fontName = 'Helvetica'
        style_data.alignment=TA_CENTER
        
        style_date = styleSheet['Normal']
        style_date.fontSize = 12
        style_date.fontName = 'Helvetica'
        style_date.alignment=TA_CENTER
        
        canvas.setTitle(document_title)
        
        contents.append(Paragraph(title, style_title))
        contents.append(Paragraph(subtitle, style_data))
        contents.append(Paragraph(fecha_actual, style_date))
        contents.append(FrameBreak())
        
        db = Data_base()
        db.connect()
        result = db.pdf_19()

        column1Heading = "NOME"
        column2Heading = "MATRÍCULA"
        column3Heading = "SETOR"
        column4Heading = "2019"
        column5Heading = "2020"
        column6Heading = "2021"
        column7Heading = "2022"
        column8Heading = "2023"

        data = [(column1Heading,column2Heading,column3Heading,column4Heading,column5Heading,column6Heading,column7Heading,column8Heading)]
        for i in range(0, len(result)):
            data.append([Paragraph(result[i][0]),Paragraph(result[i][1]),Paragraph(result[i][2]),str(result[i][3]),str(result[i][4]),str(result[i][5]),str(result[i][6]),str(result[i][7])],)
                
        tableThatSplitsOverPages = Table(data, colWidths=(3.2*inch, None, 1.6*inch, None, None, None, None, None))
        tableThatSplitsOverPages.hAlign = 'CENTER'
        tblStyle = TableStyle([('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                            ('VALIGN',(0,0),(-1,-1),'TOP'),
                            ('LINEBELOW',(0,0),(-1,-1),1,colors.black),
                            ('GRID',(0,0),(-1,-1),1,colors.black)])
        tblStyle.add('BACKGROUND',(0,0),(7,0),colors.lightblue)
        tblStyle.add('BACKGROUND',(0,1),(-1,-1),colors.white)
        tableThatSplitsOverPages.setStyle(tblStyle)
        contents.append(tableThatSplitsOverPages)   
        #contents.append(elements)
        contents.append(NextPageTemplate('laterpages'))

        contents.append(PageBreak())

        doc.addPageTemplates([firstpage,laterpages])
        doc.build(contents)
        db.close_connection()
    except:
        QMessageBox.critical(home, 'RH - CONSULTA', 'Algo não saiu como planejado!')

def pdf_20():
    try:
        webbrowser.open("Relatório.pdf")
        file_name = 'Relatório.pdf'
        document_title = 'SECRETARIA DA MULHER - SEMU'
        title = 'LISTA DE SERVIDORES DA SECRETARIA DA MULHER'
        subtitle = 'RECURSOS HUMANOS - GESTÃO DE FÉRIAS'
        day = datetime.now().strftime("%d/%m/%Y")
        fecha_actual = f'DATA DE EMISSÃO: {day}'
        
        canvas = Canvas(file_name, pagesize=A4)
        
        doc = BaseDocTemplate(file_name)
        contents =[]
        width,height = A4
        
        frame_later = Frame(
            0.2*inch,
            0.6*inch,
            (width-0.6*inch)+0.17*inch,
            height-1*inch,
            leftPadding = 0,
            topPadding=0,
            id='col'
            )
        
        frame_table= Frame(
            0.2*inch,
            0.7*inch,
            (width-0.5*inch)+0.17*inch,
            height-2*inch,
            leftPadding = 0,
            topPadding=0,
            id='col'
            )


        laterpages = PageTemplate(id='laterpages',frames=[frame_later], pagesize=A4)
        firstpage = PageTemplate(id='firstpage',frames=[ frame_later, frame_table],pagesize=A4,)

        styleSheet = getSampleStyleSheet()
        style_title = styleSheet['Heading1']
        style_title.fontSize = 14
        style_title.fontName = 'Helvetica-Bold'
        style_title.alignment=TA_CENTER
        
        style_data = styleSheet['Normal']
        style_data.fontSize = 26
        style_data.fontName = 'Helvetica'
        style_data.alignment=TA_CENTER
        
        style_date = styleSheet['Normal']
        style_date.fontSize = 12
        style_date.fontName = 'Helvetica'
        style_date.alignment=TA_CENTER
        
        canvas.setTitle(document_title)
        
        contents.append(Paragraph(title, style_title))
        contents.append(Paragraph(subtitle, style_data))
        contents.append(Paragraph(fecha_actual, style_date))
        contents.append(FrameBreak())
        
        db = Data_base()
        db.connect()
        result = db.pdf_20()


        column1Heading = "NOME"
        column2Heading = "MATRÍCULA"
        column3Heading = "SETOR"
        column4Heading = "2019"
        column5Heading = "2020"
        column6Heading = "2021"
        column7Heading = "2022"
        column8Heading = "2023"

        data = [(column1Heading,column2Heading,column3Heading,column4Heading,column5Heading,column6Heading,column7Heading,column8Heading)]
        for i in range(0, len(result)):
            data.append([Paragraph(result[i][0]),Paragraph(result[i][1]),Paragraph(result[i][2]),str(result[i][3]),str(result[i][4]),str(result[i][5]),str(result[i][6]),str(result[i][7])],)
                
        tableThatSplitsOverPages = Table(data, colWidths=(3.2*inch, None, 1.6*inch, None, None, None, None, None))
        tableThatSplitsOverPages.hAlign = 'CENTER'
        tblStyle = TableStyle([('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                            ('VALIGN',(0,0),(-1,-1),'TOP'),
                            ('LINEBELOW',(0,0),(-1,-1),1,colors.black),
                            ('GRID',(0,0),(-1,-1),1,colors.black)])
        tblStyle.add('BACKGROUND',(0,0),(7,0),colors.lightblue)
        tblStyle.add('BACKGROUND',(0,1),(-1,-1),colors.white)
        tableThatSplitsOverPages.setStyle(tblStyle)
        contents.append(tableThatSplitsOverPages)   
        #contents.append(elements)
        contents.append(NextPageTemplate('laterpages'))

        contents.append(PageBreak())

        doc.addPageTemplates([firstpage,laterpages])
        doc.build(contents)
        db.close_connection()
    except:
        QMessageBox.critical(home, 'RH - CONSULTA', 'Algo não saiu como planejado!')

def pdf_21():
    try:
        webbrowser.open("Relatório.pdf")
        file_name = 'Relatório.pdf'
        document_title = 'SECRETARIA DA MULHER - SEMU'
        title = 'LISTA DE SERVIDORES DA SECRETARIA DA MULHER'
        subtitle = 'RECURSOS HUMANOS - GESTÃO DE FÉRIAS'
        day = datetime.now().strftime("%d/%m/%Y")
        fecha_actual = f'DATA DE EMISSÃO: {day}'
        
        canvas = Canvas(file_name, pagesize=A4)
        
        doc = BaseDocTemplate(file_name)
        contents =[]
        width,height = A4
        
        frame_later = Frame(
            0.2*inch,
            0.6*inch,
            (width-0.6*inch)+0.17*inch,
            height-1*inch,
            leftPadding = 0,
            topPadding=0,
            id='col'
            )
        
        frame_table= Frame(
            0.2*inch,
            0.7*inch,
            (width-0.5*inch)+0.17*inch,
            height-2*inch,
            leftPadding = 0,
            topPadding=0,
            id='col'
            )


        laterpages = PageTemplate(id='laterpages',frames=[frame_later], pagesize=A4)
        firstpage = PageTemplate(id='firstpage',frames=[ frame_later, frame_table],pagesize=A4,)

        styleSheet = getSampleStyleSheet()
        style_title = styleSheet['Heading1']
        style_title.fontSize = 14
        style_title.fontName = 'Helvetica-Bold'
        style_title.alignment=TA_CENTER
        
        style_data = styleSheet['Normal']
        style_data.fontSize = 26
        style_data.fontName = 'Helvetica'
        style_data.alignment=TA_CENTER
        
        style_date = styleSheet['Normal']
        style_date.fontSize = 12
        style_date.fontName = 'Helvetica'
        style_date.alignment=TA_CENTER
        
        canvas.setTitle(document_title)
        
        contents.append(Paragraph(title, style_title))
        contents.append(Paragraph(subtitle, style_data))
        contents.append(Paragraph(fecha_actual, style_date))
        contents.append(FrameBreak())
        
        db = Data_base()
        db.connect()
        result = db.pdf_21()

        column1Heading = "NOME"
        column2Heading = "MATRÍCULA"
        column3Heading = "SETOR"
        column4Heading = "2019"
        column5Heading = "2020"
        column6Heading = "2021"
        column7Heading = "2022"
        column8Heading = "2023"

        data = [(column1Heading,column2Heading,column3Heading,column4Heading,column5Heading,column6Heading,column7Heading,column8Heading)]
        for i in range(0, len(result)):
            data.append([Paragraph(result[i][0]),Paragraph(result[i][1]),Paragraph(result[i][2]),str(result[i][3]),str(result[i][4]),str(result[i][5]),str(result[i][6]),str(result[i][7])],)
                
        tableThatSplitsOverPages = Table(data, colWidths=(3.2*inch, None, 1.6*inch, None, None, None, None, None))
        tableThatSplitsOverPages.hAlign = 'CENTER'
        tblStyle = TableStyle([('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                            ('VALIGN',(0,0),(-1,-1),'TOP'),
                            ('LINEBELOW',(0,0),(-1,-1),1,colors.black),
                            ('GRID',(0,0),(-1,-1),1,colors.black)])
        tblStyle.add('BACKGROUND',(0,0),(7,0),colors.lightblue)
        tblStyle.add('BACKGROUND',(0,1),(-1,-1),colors.white)
        tableThatSplitsOverPages.setStyle(tblStyle)
        contents.append(tableThatSplitsOverPages)   
        #contents.append(elements)
        contents.append(NextPageTemplate('laterpages'))

        contents.append(PageBreak())

        doc.addPageTemplates([firstpage,laterpages])
        doc.build(contents)
        db.close_connection()
    except:
        QMessageBox.critical(home, 'RH - CONSULTA', 'Algo não saiu como planejado!')

def pdf_22():
    try:
        webbrowser.open("Relatório.pdf")
        file_name = 'Relatório.pdf'
        document_title = 'SECRETARIA DA MULHER - SEMU'
        title = 'LISTA DE SERVIDORES DA SECRETARIA DA MULHER'
        subtitle = 'RECURSOS HUMANOS - GESTÃO DE FÉRIAS'
        day = datetime.now().strftime("%d/%m/%Y")
        fecha_actual = f'DATA DE EMISSÃO: {day}'
        
        canvas = Canvas(file_name, pagesize=A4)
        
        doc = BaseDocTemplate(file_name)
        contents =[]
        width,height = A4
        
        frame_later = Frame(
            0.2*inch,
            0.6*inch,
            (width-0.6*inch)+0.17*inch,
            height-1*inch,
            leftPadding = 0,
            topPadding=0,
            id='col'
            )
        
        frame_table= Frame(
            0.2*inch,
            0.7*inch,
            (width-0.5*inch)+0.17*inch,
            height-2*inch,
            leftPadding = 0,
            topPadding=0,
            id='col'
            )


        laterpages = PageTemplate(id='laterpages',frames=[frame_later], pagesize=A4)
        firstpage = PageTemplate(id='firstpage',frames=[ frame_later, frame_table],pagesize=A4,)

        styleSheet = getSampleStyleSheet()
        style_title = styleSheet['Heading1']
        style_title.fontSize = 14
        style_title.fontName = 'Helvetica-Bold'
        style_title.alignment=TA_CENTER
        
        style_data = styleSheet['Normal']
        style_data.fontSize = 26
        style_data.fontName = 'Helvetica'
        style_data.alignment=TA_CENTER
        
        style_date = styleSheet['Normal']
        style_date.fontSize = 12
        style_date.fontName = 'Helvetica'
        style_date.alignment=TA_CENTER
        
        canvas.setTitle(document_title)
        
        contents.append(Paragraph(title, style_title))
        contents.append(Paragraph(subtitle, style_data))
        contents.append(Paragraph(fecha_actual, style_date))
        contents.append(FrameBreak())
        
        db = Data_base()
        db.connect()
        result = db.pdf_22()

        column1Heading = "NOME"
        column2Heading = "MATRÍCULA"
        column3Heading = "SETOR"
        column4Heading = "2019"
        column5Heading = "2020"
        column6Heading = "2021"
        column7Heading = "2022"
        column8Heading = "2023"

        data = [(column1Heading,column2Heading,column3Heading,column4Heading,column5Heading,column6Heading,column7Heading,column8Heading)]
        for i in range(0, len(result)):
            data.append([Paragraph(result[i][0]),Paragraph(result[i][1]),Paragraph(result[i][2]),str(result[i][3]),str(result[i][4]),str(result[i][5]),str(result[i][6]),str(result[i][7])],)
                
        tableThatSplitsOverPages = Table(data, colWidths=(3.2*inch, None, 1.6*inch, None, None, None, None, None))
        tableThatSplitsOverPages.hAlign = 'CENTER'
        tblStyle = TableStyle([('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                            ('VALIGN',(0,0),(-1,-1),'TOP'),
                            ('LINEBELOW',(0,0),(-1,-1),1,colors.black),
                            ('GRID',(0,0),(-1,-1),1,colors.black)])
        tblStyle.add('BACKGROUND',(0,0),(7,0),colors.lightblue)
        tblStyle.add('BACKGROUND',(0,1),(-1,-1),colors.white)
        tableThatSplitsOverPages.setStyle(tblStyle)
        contents.append(tableThatSplitsOverPages)   
        #contents.append(elements)
        contents.append(NextPageTemplate('laterpages'))

        contents.append(PageBreak())

        doc.addPageTemplates([firstpage,laterpages])
        doc.build(contents)
        db.close_connection()
    except:
        QMessageBox.critical(home, 'RH - CONSULTA', 'Algo não saiu como planejado!')

def pdf_23():
    try:
        webbrowser.open("Relatório.pdf")
        file_name = 'Relatório.pdf'
        document_title = 'SECRETARIA DA MULHER - SEMU'
        title = 'LISTA DE SERVIDORES DA SECRETARIA DA MULHER'
        subtitle = 'RECURSOS HUMANOS - GESTÃO DE FÉRIAS'
        day = datetime.now().strftime("%d/%m/%Y")
        fecha_actual = f'DATA DE EMISSÃO: {day}'
        
        canvas = Canvas(file_name, pagesize=A4)
        
        doc = BaseDocTemplate(file_name)
        contents =[]
        width,height = A4
        
        frame_later = Frame(
            0.2*inch,
            0.6*inch,
            (width-0.6*inch)+0.17*inch,
            height-1*inch,
            leftPadding = 0,
            topPadding=0,
            id='col'
            )
        
        frame_table= Frame(
            0.2*inch,
            0.7*inch,
            (width-0.5*inch)+0.17*inch,
            height-2*inch,
            leftPadding = 0,
            topPadding=0,
            id='col'
            )


        laterpages = PageTemplate(id='laterpages',frames=[frame_later], pagesize=A4)
        firstpage = PageTemplate(id='firstpage',frames=[ frame_later, frame_table],pagesize=A4,)

        styleSheet = getSampleStyleSheet()
        style_title = styleSheet['Heading1']
        style_title.fontSize = 14
        style_title.fontName = 'Helvetica-Bold'
        style_title.alignment=TA_CENTER
        
        style_data = styleSheet['Normal']
        style_data.fontSize = 26
        style_data.fontName = 'Helvetica'
        style_data.alignment=TA_CENTER
        
        style_date = styleSheet['Normal']
        style_date.fontSize = 12
        style_date.fontName = 'Helvetica'
        style_date.alignment=TA_CENTER
        
        canvas.setTitle(document_title)
        
        contents.append(Paragraph(title, style_title))
        contents.append(Paragraph(subtitle, style_data))
        contents.append(Paragraph(fecha_actual, style_date))
        contents.append(FrameBreak())
        
        db = Data_base()
        db.connect()
        result = db.pdf_23()

        column1Heading = "NOME"
        column2Heading = "MATRÍCULA"
        column3Heading = "SETOR"
        column4Heading = "2019"
        column5Heading = "2020"
        column6Heading = "2021"
        column7Heading = "2022"
        column8Heading = "2023"

        data = [(column1Heading,column2Heading,column3Heading,column4Heading,column5Heading,column6Heading,column7Heading,column8Heading)]
        for i in range(0, len(result)):
            data.append([Paragraph(result[i][0]),Paragraph(result[i][1]),Paragraph(result[i][2]),str(result[i][3]),str(result[i][4]),str(result[i][5]),str(result[i][6]),str(result[i][7])],)
                
        tableThatSplitsOverPages = Table(data, colWidths=(3.2*inch, None, 1.6*inch, None, None, None, None, None))
        tableThatSplitsOverPages.hAlign = 'CENTER'
        tblStyle = TableStyle([('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                            ('VALIGN',(0,0),(-1,-1),'TOP'),
                            ('LINEBELOW',(0,0),(-1,-1),1,colors.black),
                            ('GRID',(0,0),(-1,-1),1,colors.black)])
        tblStyle.add('BACKGROUND',(0,0),(7,0),colors.lightblue)
        tblStyle.add('BACKGROUND',(0,1),(-1,-1),colors.white)
        tableThatSplitsOverPages.setStyle(tblStyle)
        contents.append(tableThatSplitsOverPages)   
        #contents.append(elements)
        contents.append(NextPageTemplate('laterpages'))

        contents.append(PageBreak())

        doc.addPageTemplates([firstpage,laterpages])
        doc.build(contents)
        db.close_connection()
    except:
        QMessageBox.critical(home, 'RH - CONSULTA', 'Algo não saiu como planejado!')

def circle1_on():
    try:
        db = Data_base()
        db.connect()
        all = db.select_padrao19()
        result = db.select_19()
        a = len(all)
        b = len(result)
        ab = ((b*100)/a)/100

        # PROGRESSBAR STYLESHEET BASE
        styleSheet = """
        QFrame{
            border-radius: 150px;
            background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{STOP_1} rgba(255, 0, 127, 0), stop:{STOP_2} rgba(85, 170, 255, 255));
        }
        """
        value = (b*100)/a
        # GET PROGRESS BAR VALUE, CONVERT TO FLOAT AND INVERT VALUES
        # stop works of 1.000 to 0.000
        progress = (100 - value) / 100.0

        # GET NEW VALUES
        stop_1 = str(progress - 0.001)
        stop_2 = str(progress)

        # SET VALUES TO NEW STYLESHEET
        newStylesheet = styleSheet.replace("{STOP_1}", stop_1).replace("{STOP_2}", stop_2)

        # APPLY STYLESHEET WITH NEW VALUES
        home.frame_47.setStyleSheet(newStylesheet)
        home.label_15.setText(f'{ab:.1%}')
        home.label_16.setText(f'{b} Funcionários pendentes')
    except:
        pass
    
    db.close_connection()

def circle2_on():
    db = Data_base()
    db.connect()
    try:
        all = db.select_padrao20()
        result = db.select_20()
        a = len(all)
        b = len(result)
        ab = ((b*100)/a)/100

        # PROGRESSBAR STYLESHEET BASE
        styleSheet = """
        QFrame{
            border-radius: 150px;
            background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{STOP_1} rgba(255, 0, 127, 0), stop:{STOP_2} rgba(85, 170, 255, 255));
        }
        """
        value = (b*100)/a
        # GET PROGRESS BAR VALUE, CONVERT TO FLOAT AND INVERT VALUES
        # stop works of 1.000 to 0.000
        progress = (100 - value) / 100.0

        # GET NEW VALUES
        stop_1 = str(progress - 0.001)
        stop_2 = str(progress)

        # SET VALUES TO NEW STYLESHEET
        newStylesheet = styleSheet.replace("{STOP_1}", stop_1).replace("{STOP_2}", stop_2)

        # APPLY STYLESHEET WITH NEW VALUES
        home.frame_51.setStyleSheet(newStylesheet)
        home.label_17.setText(f'{ab:.1%}')
        home.label_18.setText(f'{b} Funcionários pendentes')
    except:
        pass

    db.close_connection()

def circle3_on():
    db = Data_base()
    db.connect()
    try:
        all = db.select_padrao21()
        result = db.select_21()
        a = len(all)
        b = len(result)
        ab = ((b*100)/a)/100

        # PROGRESSBAR STYLESHEET BASE
        styleSheet = """
        QFrame{
            border-radius: 150px;
            background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{STOP_1} rgba(255, 0, 127, 0), stop:{STOP_2} rgba(85, 170, 255, 255));
        }
        """
        value = (b*100)/a
        # GET PROGRESS BAR VALUE, CONVERT TO FLOAT AND INVERT VALUES
        # stop works of 1.000 to 0.000
        progress = (100 - value) / 100.0

        # GET NEW VALUES
        stop_1 = str(progress - 0.001)
        stop_2 = str(progress)

        # SET VALUES TO NEW STYLESHEET
        newStylesheet = styleSheet.replace("{STOP_1}", stop_1).replace("{STOP_2}", stop_2)

        # APPLY STYLESHEET WITH NEW VALUES
        home.frame_55.setStyleSheet(newStylesheet)
        home.label_19.setText(f'{ab:.1%}')
        home.label_20.setText(f'{b} Funcionários pendentes')
    except:
        pass

def circle4_on():
    db = Data_base()
    db.connect()
    try:
        all = db.select_padrao22()
        result = db.select_22()
        a = len(all)
        b = len(result)
        ab = ((b*100)/a)/100

        # PROGRESSBAR STYLESHEET BASE
        styleSheet = """
        QFrame{
            border-radius: 150px;
            background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{STOP_1} rgba(255, 0, 127, 0), stop:{STOP_2} rgba(85, 170, 255, 255));
        }
        """
        value = (b*100)/a
        # GET PROGRESS BAR VALUE, CONVERT TO FLOAT AND INVERT VALUES
        # stop works of 1.000 to 0.000
        progress = (100 - value) / 100.0

        # GET NEW VALUES
        stop_1 = str(progress - 0.001)
        stop_2 = str(progress)

        # SET VALUES TO NEW STYLESHEET
        newStylesheet = styleSheet.replace("{STOP_1}", stop_1).replace("{STOP_2}", stop_2)

        # APPLY STYLESHEET WITH NEW VALUES
        home.frame_59.setStyleSheet(newStylesheet)
        home.label_21.setText(f'{ab:.1%}')
        home.label_22.setText(f'{b} Funcionários pendentes')
    except:
        pass

def circle5_on():
    db = Data_base()
    db.connect()
    try:
        all = db.select_padrao23()
        result = db.select_23()
        a = len(all)
        b = len(result)
        ab = ((b*100)/a)/100

        # PROGRESSBAR STYLESHEET BASE
        styleSheet = """
        QFrame{
            border-radius: 150px;
            background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{STOP_1} rgba(255, 0, 127, 0), stop:{STOP_2} rgba(85, 170, 255, 255));
        }
        """
        value = (b*100)/a
        # GET PROGRESS BAR VALUE, CONVERT TO FLOAT AND INVERT VALUES
        # stop works of 1.000 to 0.000
        progress = (100 - value) / 100.0

        # GET NEW VALUES
        stop_1 = str(progress - 0.001)
        stop_2 = str(progress)

        # SET VALUES TO NEW STYLESHEET
        newStylesheet = styleSheet.replace("{STOP_1}", stop_1).replace("{STOP_2}", stop_2)

        # APPLY STYLESHEET WITH NEW VALUES
        home.frame_92.setStyleSheet(newStylesheet)
        home.label_41.setText(f'{ab:.1%}')
        home.label_42.setText(f'{b} Funcionários pendentes')
    except:
        pass

def pendente_19():
    home.stackedWidget_3.setCurrentWidget(home.page_12)
    try:
        db = Data_base()
        db.connect()
        result = db.select_19()
        home.tableWidget_7.setRowCount(len(result))
        home.tableWidget_7.setColumnWidth(0,550)
        home.tableWidget_7.setColumnWidth(1,130)
        home.tableWidget_7.setColumnWidth(2,70)

        for i in range(0, len(result)):
            for j in range (0,3):
                home.tableWidget_7.setItem(i,j,QtWidgets.QTableWidgetItem(str(result[i][j])))

        db.close_connection()
    except:
        QMessageBox.critical(home, 'RH - CONSULTA', 'Algo não saiu como planejado!')

def show_pen_19():
    try:
        global id
        db = Data_base()
        db.connect()
        cursor = db.connection.cursor()
        edicao.show()
        edicao.stackedWidget.setCurrentWidget(edicao.page_5)

        line = home.tableWidget_7.currentRow()
        cursor.execute('SELECT id FROM funcionarios WHERE ano_2019 < 30 ORDER BY nome')
        dados_lidos = cursor.fetchall()
        matricula = dados_lidos[line][0]
        cursor.execute("SELECT * FROM funcionarios WHERE id="+ str(matricula) )
        show_view = cursor.fetchall()
        
        id = matricula
        
        edicao.nome.setText(str(show_view[0][1]))
        edicao.matricula.setText(str(show_view[0][2]))
        edicao.setor.setText(str(show_view[0][3]))

        edicao.dias_19.setText(str(show_view[0][4]))
        edicao.dias_20.setText(str(show_view[0][5]))
        edicao.dias_21.setText(str(show_view[0][6]))
        edicao.dias_22.setText(str(show_view[0][7]))
        edicao.dias_23.setText(str(show_view[0][8]))
    except:
        QMessageBox.critical(home, 'RH - CONSULTA', 'Algo não saiu como planejado!')

def atualiza_pendentes():
    try:
        global id
        db = Data_base()
        db.connect()
        cursor = db.connection.cursor()

        nome = edicao.nome.text().upper()
        matricula = edicao.matricula.text()
        setor = edicao.setor.text().upper()

        ano_19 = edicao.dias_19.text()
        ano_20 = edicao.dias_20.text()
        ano_21 = edicao.dias_21.text()
        ano_22 = edicao.dias_22.text()
        ano_23 = edicao.dias_23.text()

        cursor.execute("UPDATE funcionarios SET nome = '{}', matricula = '{}', setor = '{}', ano_2019 = '{}', ano_2020 = '{}', ano_2021 = '{}', ano_2022 = '{}', ano_2023 = '{}' WHERE id = '{}' ".format(nome, matricula, setor, ano_19, ano_20, ano_21, ano_22, ano_23, id) )     
        db.connection.commit()
        db.close_connection()
        
        QMessageBox.about(home, 'RH - CONSULTA', 'Cadastro Atualizado com Sucesso!')   
        
        edicao.close()
        pendente_19()        
    except:
        QMessageBox.critical(home, 'RH - CONSULTA', 'Algo não saiu como planejado!')

def pendente_20():
    home.stackedWidget_3.setCurrentWidget(home.page_18)
    try:
        db = Data_base()
        db.connect()
        result = db.select_20()
        home.tableWidget_8.setRowCount(len(result))
        home.tableWidget_8.setColumnWidth(0,550)
        home.tableWidget_8.setColumnWidth(1,130)
        home.tableWidget_8.setColumnWidth(2,70)

        for i in range(0, len(result)):
            for j in range (0,3):
                home.tableWidget_8.setItem(i,j,QtWidgets.QTableWidgetItem(str(result[i][j])))

        db.close_connection()
    except:
        QMessageBox.critical(home, 'RH - CONSULTA', 'Algo não saiu como planejado!')

def show_pen_20():
    try:
        global id
        db = Data_base()
        db.connect()
        cursor = db.connection.cursor()
        edicao.show()
        edicao.stackedWidget.setCurrentWidget(edicao.page_6)

        line = home.tableWidget_8.currentRow()
        cursor.execute('SELECT id FROM funcionarios WHERE ano_2020 < 30 ORDER BY nome')
        dados_lidos = cursor.fetchall()
        matricula = dados_lidos[line][0]
        cursor.execute("SELECT * FROM funcionarios WHERE id="+ str(matricula) )
        show_view = cursor.fetchall()
        
        id = matricula
        
        edicao.nome.setText(str(show_view[0][1]))
        edicao.matricula.setText(str(show_view[0][2]))
        edicao.setor.setText(str(show_view[0][3]))

        edicao.dias_19.setText(str(show_view[0][4]))
        edicao.dias_20.setText(str(show_view[0][5]))
        edicao.dias_21.setText(str(show_view[0][6]))
        edicao.dias_22.setText(str(show_view[0][7]))
        edicao.dias_23.setText(str(show_view[0][8]))
    except:
        QMessageBox.critical(home, 'RH - CONSULTA', 'Algo não saiu como planejado!')

def atualiza_pendentes1():
    try:
        global id
        db = Data_base()
        db.connect()
        cursor = db.connection.cursor()

        nome = edicao.nome.text().upper()
        matricula = edicao.matricula.text()
        setor = edicao.setor.text().upper()

        ano_19 = edicao.dias_19.text()
        ano_20 = edicao.dias_20.text()
        ano_21 = edicao.dias_21.text()
        ano_22 = edicao.dias_22.text()
        ano_23 = edicao.dias_23.text()

        cursor.execute("UPDATE funcionarios SET nome = '{}', matricula = '{}', setor = '{}', ano_2019 = '{}', ano_2020 = '{}', ano_2021 = '{}', ano_2022 = '{}', ano_2023 = '{}' WHERE id = '{}' ".format(nome, matricula, setor, ano_19, ano_20, ano_21, ano_22, ano_23, id) )     
        db.connection.commit()
        db.close_connection()
        
        QMessageBox.about(home, 'RH - CONSULTA', 'Cadastro Atualizado com Sucesso!')
        
        
        edicao.close()
        pendente_20()         
    except:
        QMessageBox.critical(home, 'RH - CONSULTA', 'Algo não saiu como planejado!')

def pendente_21():
    home.stackedWidget_3.setCurrentWidget(home.page_19)
    try:
        db = Data_base()
        db.connect()
        result = db.select_21()
        home.tableWidget_9.setRowCount(len(result))
        home.tableWidget_9.setColumnWidth(0,550)
        home.tableWidget_9.setColumnWidth(1,130)
        home.tableWidget_9.setColumnWidth(2,70)

        for i in range(0, len(result)):
            for j in range (0,3):
                home.tableWidget_9.setItem(i,j,QtWidgets.QTableWidgetItem(str(result[i][j])))

        db.close_connection()
    except:
        QMessageBox.critical(home, 'RH - CONSULTA', 'Algo não saiu como planejado!')

def show_pen_21():
    try:
        global id
        db = Data_base()
        db.connect()
        cursor = db.connection.cursor()
        edicao.show()
        edicao.stackedWidget.setCurrentWidget(edicao.page_7)

        line = home.tableWidget_9.currentRow()
        cursor.execute('SELECT id FROM funcionarios WHERE ano_2021 < 30 ORDER BY nome')
        dados_lidos = cursor.fetchall()
        matricula = dados_lidos[line][0]
        cursor.execute("SELECT * FROM funcionarios WHERE id="+ str(matricula) )
        show_view = cursor.fetchall()
        
        id = matricula
        
        edicao.nome.setText(str(show_view[0][1]))
        edicao.matricula.setText(str(show_view[0][2]))
        edicao.setor.setText(str(show_view[0][3]))

        edicao.dias_19.setText(str(show_view[0][4]))
        edicao.dias_20.setText(str(show_view[0][5]))
        edicao.dias_21.setText(str(show_view[0][6]))
        edicao.dias_22.setText(str(show_view[0][7]))
    except:
        QMessageBox.critical(home, 'RH - CONSULTA', 'Algo não saiu como planejado!')

def atualiza_pendentes2():
    try:
        global id
        db = Data_base()
        db.connect()
        cursor = db.connection.cursor()

        nome = edicao.nome.text().upper()
        matricula = edicao.matricula.text()
        setor = edicao.setor.text().upper()

        ano_19 = edicao.dias_19.text()
        ano_20 = edicao.dias_20.text()
        ano_21 = edicao.dias_21.text()
        ano_22 = edicao.dias_22.text()
        ano_23 = edicao.dias_23.text()

        cursor.execute("UPDATE funcionarios SET nome = '{}', matricula = '{}', setor = '{}', ano_2019 = '{}', ano_2020 = '{}', ano_2021 = '{}', ano_2022 = '{}', ano_2023 = '{}' WHERE id = '{}' ".format(nome, matricula, setor, ano_19, ano_20, ano_21, ano_22, ano_23, id) )     
        db.connection.commit()
        db.close_connection()
        
        QMessageBox.about(home, 'RH - CONSULTA', 'Cadastro Atualizado com Sucesso!')
        
        
        edicao.close()
        pendente_21()        
    except:
        QMessageBox.critical(home, 'RH - CONSULTA', 'Algo não saiu como planejado!')

def pendente_22():
    home.stackedWidget_3.setCurrentWidget(home.page_20)
    try:
        db = Data_base()
        db.connect()
        result = db.select_22()
        home.tableWidget_10.setRowCount(len(result))
        home.tableWidget_10.setColumnWidth(0,550)
        home.tableWidget_10.setColumnWidth(1,130)
        home.tableWidget_10.setColumnWidth(2,70)

        for i in range(0, len(result)):
            for j in range (0,3):
                home.tableWidget_10.setItem(i,j,QtWidgets.QTableWidgetItem(str(result[i][j])))

        db.close_connection()
    except:
        QMessageBox.critical(home, 'RH - CONSULTA', 'Algo não saiu como planejado!')

def show_pen_22():
    try:
        global id
        db = Data_base()
        db.connect()
        cursor = db.connection.cursor()
        edicao.show()
        edicao.stackedWidget.setCurrentWidget(edicao.page_9)

        line = home.tableWidget_10.currentRow()
        cursor.execute('SELECT id FROM funcionarios WHERE ano_2022 < 30 ORDER BY nome')
        dados_lidos = cursor.fetchall()
        matricula = dados_lidos[line][0]
        cursor.execute("SELECT * FROM funcionarios WHERE id="+ str(matricula) )
        show_view = cursor.fetchall()
        
        id = matricula
        
        edicao.nome.setText(str(show_view[0][1]))
        edicao.matricula.setText(str(show_view[0][2]))
        edicao.setor.setText(str(show_view[0][3]))

        edicao.dias_19.setText(str(show_view[0][4]))
        edicao.dias_20.setText(str(show_view[0][5]))
        edicao.dias_21.setText(str(show_view[0][6]))
        edicao.dias_22.setText(str(show_view[0][7]))
        edicao.dias_23.setText(str(show_view[0][8]))
    except:
        QMessageBox.critical(home, 'RH - CONSULTA', 'Algo não saiu como planejado!')

def atualiza_pendentes3():
    try:
        global id
        db = Data_base()
        db.connect()
        cursor = db.connection.cursor()

        nome = edicao.nome.text().upper()
        matricula = edicao.matricula.text()
        setor = edicao.setor.text().upper()

        ano_19 = edicao.dias_19.text()
        ano_20 = edicao.dias_20.text()
        ano_21 = edicao.dias_21.text()
        ano_22 = edicao.dias_22.text()
        ano_23 = edicao.dias_23.text()

        cursor.execute("UPDATE funcionarios SET nome = '{}', matricula = '{}', setor = '{}', ano_2019 = '{}', ano_2020 = '{}', ano_2021 = '{}', ano_2022 = '{}', ano_2023 = '{}' WHERE id = '{}' ".format(nome, matricula, setor, ano_19, ano_20, ano_21, ano_22, ano_23, id) )     
        db.connection.commit()
        db.close_connection()
        
        QMessageBox.about(home, 'RH - CONSULTA', 'Cadastro Atualizado com Sucesso!')
        
        
        edicao.close()
        pendente_22()
         
    except:
        QMessageBox.critical(home, 'RH - CONSULTAo', 'Algo não saiu como planejado!')

def pendente_23():
    home.stackedWidget_3.setCurrentWidget(home.page_13)
    try:
        db = Data_base()
        db.connect()
        result = db.select_23()
        home.tableWidget_12.setRowCount(len(result))
        home.tableWidget_12.setColumnWidth(0,550)
        home.tableWidget_12.setColumnWidth(1,130)
        home.tableWidget_12.setColumnWidth(2,70)

        for i in range(0, len(result)):
            for j in range (0,3):
                home.tableWidget_12.setItem(i,j,QtWidgets.QTableWidgetItem(str(result[i][j])))

        db.close_connection()
    except:
        QMessageBox.critical(home, 'RH - CONSULTA', 'Algo não saiu como planejado!')

def show_pen_23():
    try:
        global id
        db = Data_base()
        db.connect()
        cursor = db.connection.cursor()
        edicao.show()
        edicao.stackedWidget.setCurrentWidget(edicao.page_10)

        line = home.tableWidget_12.currentRow()
        cursor.execute('SELECT id FROM funcionarios WHERE ano_2023 < 30 ORDER BY nome')
        dados_lidos = cursor.fetchall()
        matricula = dados_lidos[line][0]
        cursor.execute("SELECT * FROM funcionarios WHERE id="+ str(matricula) )
        show_view = cursor.fetchall()
        
        id = matricula
        
        edicao.nome.setText(str(show_view[0][1]))
        edicao.matricula.setText(str(show_view[0][2]))
        edicao.setor.setText(str(show_view[0][3]))

        edicao.dias_19.setText(str(show_view[0][4]))
        edicao.dias_20.setText(str(show_view[0][5]))
        edicao.dias_21.setText(str(show_view[0][6]))
        edicao.dias_22.setText(str(show_view[0][7]))
        edicao.dias_23.setText(str(show_view[0][8]))
    except:
        QMessageBox.critical(home, 'RH - CONSULTA', 'Algo não saiu como planejado!')

def atualiza_pendentes4():
    try:
        global id
        db = Data_base()
        db.connect()
        cursor = db.connection.cursor()

        nome = edicao.nome.text().upper()
        matricula = edicao.matricula.text()
        setor = edicao.setor.text().upper()

        ano_19 = edicao.dias_19.text()
        ano_20 = edicao.dias_20.text()
        ano_21 = edicao.dias_21.text()
        ano_22 = edicao.dias_22.text()
        ano_23 = edicao.dias_23.text()

        cursor.execute("UPDATE funcionarios SET nome = '{}', matricula = '{}', setor = '{}', ano_2019 = '{}', ano_2020 = '{}', ano_2021 = '{}', ano_2022 = '{}', ano_2023 = '{}' WHERE id = '{}' ".format(nome, matricula, setor, ano_19, ano_20, ano_21, ano_22, ano_23, id) )     
        db.connection.commit()
        db.close_connection()
        
        QMessageBox.about(home, 'RH - CONSULTA', 'Cadastro Atualizado com Sucesso!')
        
        
        edicao.close()
        pendente_23()
         
    except:
        QMessageBox.critical(home, 'RH - CONSULTAo', 'Algo não saiu como planejado!')

def show1_excluir():
    try:
        global id
        db = Data_base()
        db.connect()
        cursor = db.connection.cursor()
        excluir.show()
        excluir.stackedWidget.setCurrentWidget(excluir.page)

        line = home.tableWidget.currentRow()
        cursor.execute("SELECT * FROM funcionarios ORDER BY nome")
        dados_lidos = cursor.fetchall()
        matricula = dados_lidos[line][0]
        cursor.execute(f"SELECT * FROM funcionarios WHERE id="+ str(matricula) )
        show_view = cursor.fetchall()
        
        id = matricula
        
        excluir.label_3.setText(str(show_view[0][1]))
        db.close_connection()
    except:
        QMessageBox.critical(home, 'RH - CONSULTA', 'Algo não saiu como planejado!')  

def excluir_banco():
    try:
        db = Data_base()
        db.connect()
        cursor = db.connection.cursor()
        
        excluir.show()
        excluir.stackedWidget.setCurrentWidget(excluir.page)

        line = home.tableWidget.currentRow()
        home.tableWidget.removeRow(line)
        cursor.execute("SELECT * FROM funcionarios ORDER BY nome")
        dados = cursor.fetchall()
        matricula = dados[line][0]
        cursor.execute("DELETE FROM funcionarios WHERE id="+ str(matricula))

        excluir.close()
        db.connection.commit()
        db.close_connection()
    except:
        QMessageBox.critical(home, 'RH - CONSULTA', 'Algo não saiu como planejado!') 

def show2_excluir():
    try:
        global id
        db = Data_base()
        db.connect()
        cursor = db.connection.cursor()
        excluir.show()
        excluir.stackedWidget.setCurrentWidget(excluir.page_2)

        busca = home.buscar.text().upper()

        line = home.tableWidget.currentRow()
        cursor.execute("SELECT id FROM funcionarios WHERE nome LIKE '%{}%' ORDER BY nome".format(busca))
        dados_lidos = cursor.fetchall()
        matricula = dados_lidos[line][0]
        cursor.execute("SELECT * FROM funcionarios WHERE id="+ str(matricula) )
        show_view = cursor.fetchall()
        
        id = matricula
        
        excluir.label_3.setText(str(show_view[0][1]))
        db.close_connection()
    except:
        QMessageBox.critical(home, 'RH - CONSULTA', 'Algo não saiu como planejado!')  

def excluir_banco2():
    try:
        db = Data_base()
        db.connect()
        cursor = db.connection.cursor()
       
        busca = home.buscar.text().upper()

        excluir.show()
        excluir.stackedWidget.setCurrentWidget(excluir.page_2)

        line = home.tableWidget.currentRow()
        home.tableWidget.removeRow(line)
        cursor.execute("SELECT * FROM funcionarios WHERE nome LIKE '%{}%' ORDER BY nome".format(busca))
        dados = cursor.fetchall()
        matricula = dados[line][0]
        cursor.execute("DELETE FROM funcionarios WHERE id="+ str(matricula))

        excluir.close()
        db.connection.commit()
        db.close_connection()
    except:
        QMessageBox.critical(home, 'RH - CONSULTA', 'Algo não saiu como planejado!') 

def show3_excluir():
    try:
        global id
        db = Data_base()
        db.connect()
        cursor = db.connection.cursor()
        excluir.show()
        excluir.stackedWidget.setCurrentWidget(excluir.page_3)

        busca = home.buscar_2.text()

        line = home.tableWidget.currentRow()
        cursor.execute("SELECT id FROM funcionarios WHERE matricula LIKE '%{}%' ORDER BY nome".format(busca))
        dados_lidos = cursor.fetchall()
        matricula = dados_lidos[line][0]
        cursor.execute("SELECT * FROM funcionarios WHERE id="+ str(matricula) )
        show_view = cursor.fetchall()
        
        id = matricula
        
        excluir.label_3.setText(str(show_view[0][1]))
        db.close_connection()
    except:
        QMessageBox.critical(home, 'RH - CONSULTA', 'Algo não saiu como planejado!')  

def excluir_banco3():
    try:
        db = Data_base()
        db.connect()
        cursor = db.connection.cursor()
       
        busca = home.buscar_2.text()

        excluir.show()
        excluir.stackedWidget.setCurrentWidget(excluir.page_3)

        line = home.tableWidget.currentRow()
        home.tableWidget.removeRow(line)
        cursor.execute("SELECT * FROM funcionarios WHERE matricula LIKE '%{}%' ORDER BY nome".format(busca))
        dados = cursor.fetchall()
        matricula = dados[line][0]
        cursor.execute("DELETE FROM funcionarios WHERE id="+ str(matricula))

        excluir.close()
        db.connection.commit()
        db.close_connection()
    except:
        QMessageBox.critical(home, 'RH - CONSULTA', 'Algo não saiu como planejado!') 

def show4_excluir():
    try:
        global id
        db = Data_base()
        db.connect()
        cursor = db.connection.cursor()
        excluir.show()
        excluir.stackedWidget.setCurrentWidget(excluir.page_4)

        busca = home.buscar.text().upper()

        line = home.tableWidget.currentRow()
        cursor.execute("SELECT id FROM funcionarios WHERE setor LIKE '%{}%' ORDER BY nome".format(busca))
        dados_lidos = cursor.fetchall()
        matricula = dados_lidos[line][0]
        cursor.execute("SELECT * FROM funcionarios WHERE id="+ str(matricula) )
        show_view = cursor.fetchall()
        
        id = matricula
        
        excluir.label_3.setText(str(show_view[0][1]))
        db.close_connection()
    except:
        QMessageBox.critical(home, 'RH - CONSULTA', 'Algo não saiu como planejado!')  

def excluir_banco4():
    try:
        db = Data_base()
        db.connect()
        cursor = db.connection.cursor()
       
        busca = home.buscar.text().upper()

        excluir.show()
        excluir.stackedWidget.setCurrentWidget(excluir.page_4)

        line = home.tableWidget.currentRow()
        home.tableWidget.removeRow(line)
        cursor.execute("SELECT * FROM funcionarios WHERE setor LIKE '%{}%' ORDER BY nome".format(busca))
        dados = cursor.fetchall()
        matricula = dados[line][0]
        cursor.execute("DELETE FROM funcionarios WHERE id="+ str(matricula))

        excluir.close()
        db.connection.commit()
        db.close_connection()
    except:
        QMessageBox.critical(home, 'RH - CONSULTA', 'Algo não saiu como planejado!') 

def cancelar():
    excluir.close()

def gerar_excel():
    try:
        path_name  = filedialog.askdirectory()
        
        cnx = sqlite3.connect("system.db")
        result = pd.read_sql_query("""SELECT * FROM funcionarios ORDER BY nome""", cnx)

        result.to_excel(f"{path_name}/controle_férias.xlsx", sheet_name='controle', index=False)
        
        QMessageBox.about(home, 'RH - CONSULTA', ' Planilha gerada com Sucesso! \n')
    except:
        QMessageBox.critical(home, 'RH - CONSULTA', ' A planilha não pode ser gerada! \n')

def dash():
    db = Data_base()
    db.connect()
    result = db.select_all()
    a = len(result)
    if result == []:
        QMessageBox.about(home, 'RH - CONSULTA', ' NÃO EXISTE DADOS PARA FAZER ESTATÍSTICA! \n')
        Go_home()
    else:
        home.label_25.setText(str(a))
        home.label_26.setText("FUNCIONÁRIOS CADASTRADOS NO SISTEMA")

app = QtWidgets.QApplication([])

# Janelas
home = uic.loadUi('main.ui')
edicao = uic.loadUi('atualizacao.ui')
excluir = uic.loadUi('excluir.ui')

home.stackedWidget.setCurrentWidget(home.page)

Run_ing = QtCore.QTimer()
Run_ing.timeout.connect(circle1_on)
Run_ing.start(1000)

Run_ing2 = QtCore.QTimer()
Run_ing2.timeout.connect(circle2_on)
Run_ing2.start(1000)

Run_ing3 = QtCore.QTimer()
Run_ing3.timeout.connect(circle3_on)
Run_ing3.start(1000)

Run_ing4 = QtCore.QTimer()
Run_ing4.timeout.connect(circle4_on)
Run_ing4.start(1000)

Run_ing5 = QtCore.QTimer()
Run_ing5.timeout.connect(circle5_on)
Run_ing5.start(1000)

 
############# TELA HOME #########################
home.go_home.clicked.connect(Go_home)
home.go_Cadastro.clicked.connect(Tela_Cadastro)
home.go_Consulta.clicked.connect(Tela_Consulta)
home.go_Dashboard.clicked.connect(Tela_Dashboard)
home.go_Dashboard.clicked.connect(dash)
home.go_Relatorios.clicked.connect(Tela_Relatorios)
home.input_matricula.setValidator(QIntValidator())
home.buscar_2.setValidator(QIntValidator())

############# TELA CADASTRO #####################
# Botão salvar (CADASTRO)
home.salvar.clicked.connect(selacao_1)
home.salvar.clicked.connect(selacao_2)
home.salvar.clicked.connect(selacao_3)
home.salvar.clicked.connect(selacao_4)
home.salvar.clicked.connect(selacao_5)
home.salvar.clicked.connect(Cadastrar)

############# TELA CONSULTA #####################

home.all.clicked.connect(Consulta_all) # Botão ALL
home.busca.clicked.connect(Consulta_filtro) # Botão de BUSCA (lupa)
home.filtro.currentIndexChanged.connect(index_changed)  

# Botão de EDITAR
home.atualizar_4.clicked.connect(show_all)
home.atualizar_4.clicked.connect(edicao_1)
home.atualizar_4.clicked.connect(edicao_2)
home.atualizar_4.clicked.connect(edicao_3)
home.atualizar_4.clicked.connect(edicao_4)
home.atualizar_4.clicked.connect(edicao_5)

home.atualizar_5.clicked.connect(show_nome)
home.atualizar_5.clicked.connect(edicao_1)
home.atualizar_5.clicked.connect(edicao_2)
home.atualizar_5.clicked.connect(edicao_3)
home.atualizar_5.clicked.connect(edicao_4)
home.atualizar_5.clicked.connect(edicao_5)

home.atualizar_6.clicked.connect(show_matricula)
home.atualizar_6.clicked.connect(edicao_1)
home.atualizar_6.clicked.connect(edicao_2)
home.atualizar_6.clicked.connect(edicao_3)
home.atualizar_6.clicked.connect(edicao_4)
home.atualizar_6.clicked.connect(edicao_5)

home.atualizar_7.clicked.connect(show_setor)
home.atualizar_7.clicked.connect(edicao_1)
home.atualizar_7.clicked.connect(edicao_2)
home.atualizar_7.clicked.connect(edicao_3)
home.atualizar_7.clicked.connect(edicao_4)
home.atualizar_7.clicked.connect(edicao_5)

home.relatorio_4.clicked.connect(pdf_all)
home.relatorio_5.clicked.connect(pdf_nome)
home.relatorio_6.clicked.connect(pdf_matricula)
home.relatorio_7.clicked.connect(pdf_setor)

home.excluir.clicked.connect(show1_excluir)
home.excluir_nome.clicked.connect(show2_excluir)
home.excluir_matricula.clicked.connect(show3_excluir)
home.excluir_setor.clicked.connect(show4_excluir)

############# TELA EXCLUIR ###################
excluir.sim.clicked.connect(excluir_banco)
excluir.nao.clicked.connect(cancelar)
excluir.sim_2.clicked.connect(excluir_banco2)
excluir.nao_2.clicked.connect(cancelar)
excluir.sim_3.clicked.connect(excluir_banco3)
excluir.nao_3.clicked.connect(cancelar)
excluir.sim_4.clicked.connect(excluir_banco4)
excluir.nao_4.clicked.connect(cancelar)

############# TELA DASHBOARD ###################
home.busca_19.clicked.connect(pendente_19)
home.voltar_19.clicked.connect(Tela_Dashboard)
home.atualizar_19.clicked.connect(show_pen_19)
home.atualizar_19.clicked.connect(edicao_1)
home.atualizar_19.clicked.connect(edicao_2)
home.atualizar_19.clicked.connect(edicao_3)
home.atualizar_19.clicked.connect(edicao_4)
home.atualizar_19.clicked.connect(edicao_5)

home.busca_20.clicked.connect(pendente_20)
home.voltar_2.clicked.connect(Tela_Dashboard)
home.atualizar_20.clicked.connect(show_pen_20)
home.atualizar_20.clicked.connect(edicao_1)
home.atualizar_20.clicked.connect(edicao_2)
home.atualizar_20.clicked.connect(edicao_3)
home.atualizar_20.clicked.connect(edicao_4)
home.atualizar_20.clicked.connect(edicao_5)

home.busca_21.clicked.connect(pendente_21)
home.voltar_21.clicked.connect(Tela_Dashboard)
home.atualizar_21.clicked.connect(show_pen_21)
home.atualizar_21.clicked.connect(edicao_1)
home.atualizar_21.clicked.connect(edicao_2)
home.atualizar_21.clicked.connect(edicao_3)
home.atualizar_21.clicked.connect(edicao_4)
home.atualizar_21.clicked.connect(edicao_5)

home.buscar_22.clicked.connect(pendente_22)
home.voltar_22.clicked.connect(Tela_Dashboard)
home.atualizar_22.clicked.connect(show_pen_22)
home.atualizar_22.clicked.connect(edicao_1)
home.atualizar_22.clicked.connect(edicao_2)
home.atualizar_22.clicked.connect(edicao_3)
home.atualizar_22.clicked.connect(edicao_4)
home.atualizar_22.clicked.connect(edicao_5)

home.busca_23.clicked.connect(pendente_23)
home.voltar_24.clicked.connect(Tela_Dashboard)
home.atualizar_23.clicked.connect(show_pen_23)
home.atualizar_23.clicked.connect(edicao_1)
home.atualizar_23.clicked.connect(edicao_2)
home.atualizar_23.clicked.connect(edicao_3)
home.atualizar_23.clicked.connect(edicao_4)
home.atualizar_23.clicked.connect(edicao_5)

############# TELA RELATÓRO #####################
home.pdf_1.clicked.connect(pdf_all)
home.pdf_2.clicked.connect(pdf_19)
home.pdf_3.clicked.connect(pdf_20)
home.pdf_4.clicked.connect(pdf_21)
home.pdf_5.clicked.connect(pdf_22)
home.pdf_7.clicked.connect(pdf_23)
home.pdf_6.clicked.connect(gerar_excel)

############# TELA EDIÇÃO #####################
edicao.update.clicked.connect(atualizacao_1)
edicao.update.clicked.connect(atualizacao_2)
edicao.update.clicked.connect(atualizacao_3)
edicao.update.clicked.connect(atualizacao_4)
edicao.update.clicked.connect(atualizacao_5)
edicao.update.clicked.connect(atualiza_all)

edicao.update_2.clicked.connect(atualizacao_1)
edicao.update_2.clicked.connect(atualizacao_2)
edicao.update_2.clicked.connect(atualizacao_3)
edicao.update_2.clicked.connect(atualizacao_4)
edicao.update_2.clicked.connect(atualizacao_5)
edicao.update_2.clicked.connect(atualiza_all)

edicao.update_3.clicked.connect(atualizacao_1)
edicao.update_3.clicked.connect(atualizacao_2)
edicao.update_3.clicked.connect(atualizacao_3)
edicao.update_3.clicked.connect(atualizacao_4)
edicao.update_3.clicked.connect(atualizacao_5)
edicao.update_3.clicked.connect(atualiza_all)

edicao.update_4.clicked.connect(atualizacao_1)
edicao.update_4.clicked.connect(atualizacao_2)
edicao.update_4.clicked.connect(atualizacao_3)
edicao.update_4.clicked.connect(atualizacao_4)
edicao.update_4.clicked.connect(atualizacao_5)
edicao.update_4.clicked.connect(atualiza_all)

#--------------------------------------------
edicao.update_5.clicked.connect(atualizacao_1)
edicao.update_5.clicked.connect(atualizacao_2)
edicao.update_5.clicked.connect(atualizacao_3)
edicao.update_5.clicked.connect(atualizacao_4)
edicao.update_5.clicked.connect(atualizacao_5)
edicao.update_5.clicked.connect(atualiza_pendentes)

edicao.update_6.clicked.connect(atualizacao_1)
edicao.update_6.clicked.connect(atualizacao_2)
edicao.update_6.clicked.connect(atualizacao_3)
edicao.update_6.clicked.connect(atualizacao_4)
edicao.update_6.clicked.connect(atualizacao_5)
edicao.update_6.clicked.connect(atualiza_pendentes1)

edicao.update_7.clicked.connect(atualizacao_1)
edicao.update_7.clicked.connect(atualizacao_2)
edicao.update_7.clicked.connect(atualizacao_3)
edicao.update_7.clicked.connect(atualizacao_4)
edicao.update_7.clicked.connect(atualizacao_5)
edicao.update_7.clicked.connect(atualiza_pendentes2)

edicao.update_9.clicked.connect(atualizacao_1)
edicao.update_9.clicked.connect(atualizacao_2)
edicao.update_9.clicked.connect(atualizacao_3)
edicao.update_9.clicked.connect(atualizacao_4)
edicao.update_9.clicked.connect(atualizacao_5)
edicao.update_9.clicked.connect(atualiza_pendentes3)

edicao.update_10.clicked.connect(atualizacao_1)
edicao.update_10.clicked.connect(atualizacao_2)
edicao.update_10.clicked.connect(atualizacao_3)
edicao.update_10.clicked.connect(atualizacao_4)
edicao.update_10.clicked.connect(atualizacao_5)
edicao.update_10.clicked.connect(atualiza_pendentes4)

backup()
db = Data_base()
db.connect()
db.create_table()
db.close_connection()

home.showMaximized()
app.exec()
