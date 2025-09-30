from __future__ import print_function
from datetime import date, datetime, timedelta
import mysql.connector
import json


cnx = mysql.connector.connect(
    user="root",
    password="",
    host="127.0.0.1",
    port=3306,  # <-- ajuste se a porta for outra
    database="produtos_db"
)
cursor = cnx.cursor()

tomorrow = datetime.now().date() + timedelta(days=1)    

cnx = mysql.connector.connect(user='', database='produtos_db')
cursor = cnx.cursor()

tomorrow = datetime.now().date() + timedelta(days=1)


add_produto = ("INSERT INTO produtos "
               "(nome, preco, mercado) "
               "VALUES (%s, %s, %s)")


with open('paodeacucar_all_pages.json', 'r',encoding='utf-8') as arquivo:
    dados = json.load(arquivo)



    for produto in dados:
        info_produto = (
            produto["nome"],
            produto["preco"],
            produto["mercado"]
        )
        cursor.execute(add_produto,info_produto)

# Insert new employee


# Insert new employee
cursor.execute(add_produto)

emp_no = cursor.lastrowid

# Insert salary information



# Make sure data is committed to the database
cnx.commit()
cursor.execute("SELECT * FROM produtos")
resultados = cursor.fetchall()

for linha in resultados:
    print(linha)
print(f"{cursor.rowcount} registros inseridos.")
cursor.close()
cnx.close()
