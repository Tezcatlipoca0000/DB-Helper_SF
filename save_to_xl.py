def copy_price():
    import fdb
    import pandas as pd
    import datetime

    excel_df = pd.read_excel('Provedores Todos.xlsm', sheet_name='Datos', index_col=0, na_values='--', skipfooter=10, usecols='A:AE')
    con = fdb.connect(dsn="localhost:C:/Users/casa/Desktop/DB-Helper/PDVDATA.FDB", user='SYSDBA', password='masterkey', charset='UTF8')
    cur = con.cursor()

    for idx, row in excel_df.iterrows():
        pp_set = set()
        excel_df.loc[idx, 'PVENTA'] = ''
        if pd.notna(row['Código de Barras']):
            x = str(row['Código de Barras']).upper()
            if ',' in x:
                xx = x.split(',')
                for x in xx:
                    x = x.strip()
                    cur.execute("SELECT PVENTA FROM PRODUCTOS WHERE CODIGO = ?;", (x.encode('utf-8'),))
                    pp = cur.fetchone()
                    if pp : pp_set.add(pp[0])
            else:
                cur.execute("SELECT PVENTA FROM PRODUCTOS WHERE CODIGO = ?;", (x.encode('utf-8'),))
                pp = cur.fetchone()
                if pp : pp_set.add(pp[0])
        if pd.notna(row['Código SuperFuentes']):
            x = str(row['Código SuperFuentes']).upper()
            if ',' in x:
                xx = x.split(',')
                for x in xx:
                    x = x.strip()
                    cur.execute("SELECT PVENTA FROM PRODUCTOS WHERE CODIGO = ?;", (x.encode('utf-8'),))
                    pp = cur.fetchone()
                    if pp : pp_set.add(pp[0])
            else:
                cur.execute("SELECT PVENTA FROM PRODUCTOS WHERE CODIGO = ?;", (x.encode('utf-8'),))
                pp = cur.fetchone()
                if pp : pp_set.add(pp[0])
        if len(pp_set) > 1:
            for i in pp_set:
                excel_df.loc[idx, 'PVENTA'] = excel_df.loc[idx, 'PVENTA'] + str(i) + ', '
            excel_df.loc[idx, 'Última Rev. Precios'] = datetime.date.today()
        elif len(pp_set) == 1:
            for i in pp_set:
                excel_df.loc[idx, 'PVENTA'] = str(i) 
            excel_df.loc[idx, 'Última Rev. Precios'] = datetime.date.today()
    
    con.close()
    with pd.ExcelWriter('updated-price.xlsx') as writer:
        excel_df.to_excel(writer)