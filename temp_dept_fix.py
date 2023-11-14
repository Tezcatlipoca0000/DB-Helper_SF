import fdb

con = fdb.connect(dsn="localhost:C:/Users/casa/Desktop/DB-Helper/PDVDATA.FDB", user='SYSDBA', password='masterkey')
cur = con.cursor()

bkup_prov = {'- Sin Departamento -': 3, 'Sin Departamento': 2, 'Productos Comunes': 5, 'Bimbo Blanco': 6, 'Bimbo Dulce': 7, 'Barcel': 8, 'Sabritas': 9, 'Leo': 10, 'Encanto': 11, 'Bokados': 12, 'Marinela Pastel': 13, 'Ricolino': 14, 'Lala': 15, 'Coca-Cola': 16, 'Pepsi': 17, 'Bonafont Botella': 18, 'bonafon garrafon (Eliminado 08/12/2022)': 19, 'Peñafiel': 20, 'valle (Eliminado 08/12/2022)': 21, 'Gamesa': 22, 'Treviño': 23, 'tang (Eliminado 08/12/2022)': 24, 'Tía Rosa': 25, 'Tostitos': 26, 'Sigma': 27, 'Verdura': 28, '59 (Eliminado 08/12/2022)': 29, 'Del Valle': 30, 'Pall Mall': 31, 'Bonafont Garrafon': 32, 'Varios': 33, 'Bimbo Totopos': 34, 'Marinela Galleta': 35, 'Tostadas Norteñas': 36, 'Especias': 37, 'Hielati': 38, 'Kinder': 39, 'Marlboro': 40}
rvrsd_bkup = {v: k for k, v in bkup_prov.items()}

for key in rvrsd_bkup:
    cur.execute("UPDATE DEPARTAMENTOS SET NOMBRE = ? WHERE ID = ?;", (rvrsd_bkup[key], key))
    con.commit()

cur.execute("SELECT * FROM DEPARTAMENTOS;")
x = cur.fetchall()
print(x)
con.close()
