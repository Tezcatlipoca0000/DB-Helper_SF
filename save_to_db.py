def update_db(dict_prov : dict, exclude : list = [], include : list = [], enforce : bool = False):

    '''
    Function to save FROM a backup_database in an excel file TO PDVDATA.FDB

    Parameters:
        - dict_prov: {"Name": ID}
            Required: Yes
            Default: N/A
            Is the key value pair of name and id of the DEPARTAMENTOS table sorted in a dictionary.
            Obtain the dictionary from get_prov.py
        - exclude: ["Provedor", ...]
            Required: No
            Default: []
            Is a list of valid names that match those in the dict_prov dictionary. All the names provided will be 
            excluded from manipulation.
        - include: ["Provedor", ...]
            Required: No
            Default: []
            Is a list of valid names that match those in the dict_prov dictionary. All the names provided will be
            the only to be manipulated
        - enforce: False | True
            Required: No
            Default: False
            Enforce update of every value in the DB without checking dates
            
    '''

    import fdb
    import pandas as pd
    import datetime

    excel_df = pd.read_excel('Provedores Todos.xlsm', sheet_name='Datos', index_col=0, na_values='--', skipfooter=10, usecols='A:AE')
    con = fdb.connect(dsn="localhost:C:/Users/casa/Desktop/DB-Helper/PDVDATA.FDB", user='SYSDBA', password='masterkey')
    cur = con.cursor()
    date = datetime.date.today()
    updated = []
    inserted = []
    skipped = []

    def fix_row(code, row):
        cur.execute( "UPDATE PRODUCTOS SET DESCRIPCION = ? WHERE CODIGO = ?;", (row['Producto'], code) )
        cur.execute("SELECT * FROM PRODUCTOS WHERE CODIGO = ?;", (code,))
        try:
            x = cur.fetchone()
        except:
            x = 'error'
        return x

    def update_or_insert(code, row):
        #print('Begin operation on code:', code)

        cur.execute( "SELECT * FROM PRODUCTOS WHERE CODIGO = ?;", (code,) )
        try:
            x = cur.fetchone()
        except Exception as e:
            x = fix_row(code=code, row=row)
        finally:
            if x == 'error': # Error detected in DB and NOT fixed
                #print('Skipping PDV row due to an error that could not be fixed')
                skipped.append(code)
            elif not x: # No row found. Insert into DB
                #print('no data found on DB. Proceding to insert')
                # define profit
                profit = float(row['Margen']) * 100 if pd.notna(row['Margen']) else 0
                #insert
                cur.execute( "INSERT INTO PRODUCTOS (CHECADO_EN, CODIGO, DESCRIPCION, TVENTA, PCOSTO, PVENTA, DEPT, PROVID, UMEDIDA, MAYOREO, IPRIORIDAD, DINVENTARIO, DINVMINIMO, DINVMAXIMO, PORCENTAJE_GANANCIA, COMPONENTES, IMPUESTOS, PVENTA_ANTERIOR, PCOSTO_ANTERIOR, PMAYOREO_ANTERIOR) VALUES (?, ?, ?, ?, ?, ?, ?, 0, 0, 0.0, 0, 0.0, 0, 0, ?, '', '', 0.0, 0.0, 0.0)", (date, code, row['Producto'], row['TVENTA'], float(row['Costo Unitario']), float(row['Precio al Público']), int(dict_prov[row['Provedor']]), int(profit)) )
                con.commit()
                #print('Inserted new row')
                inserted.append(code)
            else: # Row found. Update DB
                if enforce:
                    cost = row['Costo Unitario'] if pd.notna(row['Costo Unitario']) else x[3] if x[3] else 0.0
                    old_cost = x[3] if row['Costo Unitario'] != x[3] else x[18] if x[18] else 0.0
                    price = row['Precio al Público'] if pd.notna(row['Precio al Público']) else x[4] if x[4] else 0.0
                    old_price = x[4] if row['Precio al Público'] != x[4] else x[17] if x[17] else 0.0
                else:
                    # Compare dates
                    db_date = x[13] if x[13] else datetime.date(1900, 1, 1)
                    xl_cost_date = pd.Timestamp(row['Última Rev. Costos']).date() if not pd.isnull(row['Última Rev. Costos']) else datetime.date(1900, 1, 1)
                    xl_price_date = pd.Timestamp(row['Última Rev. Precios']).date() if not pd.isnull(row['Última Rev. Precios']) else datetime.date(1900, 1, 1)
                    # define cost and old_cost
                    if xl_cost_date <= db_date:
                        #print('skiping update of cost in DB')
                        cost = x[3] if x[3] else row['Costo Unitario'] if pd.notna(row['Costo Unitario']) else 0.0
                        old_cost = x[18] if x[18] else 0.0
                    else:
                        cost = row['Costo Unitario'] if pd.notna(row['Costo Unitario']) else x[3] if x[3] else 0.0
                        old_cost = x[3] if x[3] and pd.notna(row['Costo Unitario']) else x[18] if x[18] else 0.0
                        #print('Going to update cost in DB')
                    # define price and old_price
                    if xl_price_date <= db_date:
                        #print('skiping update of price in DB')
                        price = x[4] if x[4] else row['Precio al Público'] if pd.notna(row['Precio al Público']) else 0.0
                        old_price = x[17] if x[17] else 0.0
                    else:
                        price = row['Precio al Público'] if pd.notna(row['Precio al Público']) else x[4] if x[4] else 0.0
                        old_price = x[4] if x[4] and pd.notna(row['Precio al Público']) else x[17] if x[17] else 0.0
                        #print('Going to update price in DB')
                # define profit
                try:
                    profit = ((price - cost) / cost) * 100
                except ZeroDivisionError:
                    profit = 0
                #update
                cur.execute( "UPDATE PRODUCTOS SET CHECADO_EN = ?, DESCRIPCION = ?, PCOSTO = ?, PVENTA = ?, DEPT = ?, PORCENTAJE_GANANCIA = ?, PVENTA_ANTERIOR = ?, PCOSTO_ANTERIOR = ? WHERE CODIGO = ?;", (date, row['Producto'], float(cost), float(price), int(dict_prov[row['Provedor']]), int(profit), float(old_price), float(old_cost), code) )
                con.commit()
                #print('Updated row')
                updated.append(code)
                

    for idx, row in excel_df.iterrows():
        if include:
            if row['Provedor'] in include:
                if row['Provedor'] in exclude: continue
                if pd.notna(row['Código de Barras']):
                    x = str(row['Código de Barras']).upper()
                    if ',' in x:
                        xx = x.split(',')
                        for x in xx:
                            x = x.strip()
                            update_or_insert(code=x, row=row)
                    else:
                        update_or_insert(code=x, row=row)
                if pd.notna(row['Código SuperFuentes']):
                    x = str(row['Código SuperFuentes']).upper()
                    if ',' in x:
                        xx = x.split(',')
                        for x in xx:
                            x = x.strip()
                            update_or_insert(code=x, row=row)
                    
        else:
            if row['Provedor'] in exclude: continue
            if pd.notna(row['Código de Barras']):
                x = str(row['Código de Barras']).upper()
                if ',' in x:
                    xx = x.split(',')
                    for x in xx:
                        x = x.strip()
                        update_or_insert(code=x, row=row)
                else:
                    update_or_insert(code=x, row=row)
            if pd.notna(row['Código SuperFuentes']):
                x = str(row['Código SuperFuentes']).upper()
                if ',' in x:
                        xx = x.split(',')
                        for x in xx:
                            x = x.strip()
                            update_or_insert(code=x, row=row)
    

    con.close()
    print('Finished!')
    print('skipped:', len(skipped))
    print('inserted:', len(inserted))
    print('updated:', len(updated))
