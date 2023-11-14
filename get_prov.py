def get_prov():
    '''
    A function to retrieve a dictionary of providers {"name": id}
    No arguments necessary
    '''
    import fdb

    con = fdb.connect(dsn="localhost:C:/Users/casa/Desktop/DB-Helper/PDVDATA.FDB", user='SYSDBA', password='masterkey')
    cur = con.cursor()
    dict_prov = dict()
    err_idx = list()
    err_ids = list()
    err_dict = dict()

    # Backup Info
    ###########
    bkup_prov = {'- Sin Departamento -': 3, 'Sin Departamento': 2, 'Productos Comunes': 5, 'Bimbo Blanco': 6, 'Bimbo Dulce': 7, 'Barcel': 8, 'Sabritas': 9, 'Leo': 10, 'Encanto': 11, 'Bokados': 12, 'Marinela Pastel': 13, 'Ricolino': 14, 'Lala': 15, 'Coca-Cola': 16, 'Pepsi': 17, 'Bonafont Botella': 18, 'bonafon garrafon (Eliminado 08/12/2022)': 19, 'Peñafiel': 20, 'valle (Eliminado 08/12/2022)': 21, 'Gamesa': 22, 'Treviño': 23, 'tang (Eliminado 08/12/2022)': 24, 'Tía Rosa': 25, 'Tostitos': 26, 'Sigma': 27, 'Verdura': 28, '59 (Eliminado 08/12/2022)': 29, 'Del Valle': 30, 'Pall Mall': 31, 'Bonafont Garrafon': 32, 'Varios': 33, 'Bimbo Totopos': 34, 'Marinela Galleta': 35, 'Tostadas Norteñas': 36, 'Especias': 37, 'Hielati': 38, 'Kinder': 39, 'Marlboro': 40}
    rvrsd_bkup = {v: k for k, v in bkup_prov.items()}

    # 1.- Get list of indexes where there's an exception and first draft the dict_prov
    ###########
    cur.execute("SELECT * FROM DEPARTAMENTOS;")
    for i in range(200):
        try:
            x = cur.fetchone()
            if not x: break
            dict_prov[x[1]] = x[0]
        except Exception as e:
            #print(f'1.- Error in row {i} captured ----> \n', e)
            err_idx.append(i)
            err_dict[f'row{i}'] = e

    # 2.- Get list of id's that correspond to index of error
    ###########
    cur.execute("SELECT ID FROM DEPARTAMENTOS;")
    for i in range(200):
        try:
            x = cur.fetchone()
            if not x: break
            if i in err_idx:
                err_ids.append(x[0])
        except Exception as e:
            #print('2.- Error in ID column captured ----> \n', e)
            err_dict[f'row{i}'] = e

    # 3.- if faulty name exist in backup then re-write the name in the DB and add to dict_prov
    ###########
    for id in err_ids:
        if id in bkup_prov.values():
            cur.execute("UPDATE DEPARTAMENTOS SET NOMBRE = ? WHERE ID = ?;", (rvrsd_bkup[id], id) )
            dict_prov[rvrsd_bkup[id]] = id
            err_dict[f'id:{id}'] = f'fixed name: {rvrsd_bkup[id]}'
            con.commit()
        else:
            err_dict[f'id_not_found:{id}'] = f'id with error not in backup: {id}'
    
    con.close()
    #print('exiting get_prov....', dict_prov)
    return {'data': dict_prov, 'errors': err_dict}
