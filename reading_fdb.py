# testing reading a Firebird database file

import fdb

con = fdb.connect(dsn="localhost:C:/Tez/testing/PDVDATA.FDB", user='SYSDBA', password='masterkey')

cur = con.cursor()

#cur.execute("SELECT DESCRIPCION FROM PRODUCTOS WHERE DEPT = 18;")
# select rdb$field_name from rdb$relation_fields where rdb$relation_name='YOUR-TABLE_NAME';
cur.execute("select rdb$field_name from rdb$relation_fields where rdb$relation_name='DEPTS'")

print(cur.fetchall())

'''
TABLES:
 ABONOS                                 CAJAS
 CLIENTES                               CONFIGURACION
 CORTE_IMPUESTOS_COBRADOS               CORTE_IMP_COBRADOS_OPERACION
 CORTE_MOVIMIENTOS                      CORTE_OPERACIONES
 CORTE_VENTAS_DEPTO_OPERACIONES         CORTE_VENTAS_POR_DEPTO
 DEPARTAMENTOS                          DEPTS
 FACTURACION_CERTIFICADOS               FACTURACION_CLIENTES
 FACTURACION_EMISORES                   FACTURACION_FOLIOS
 FACTURACION_INFORMES                   FACTURAS
 HISTORIAL_INVENTARIO                   HISTORIAL_USUARIOS
 IMPUESTOS                              MEDIDAS
 MOVIMIENTOS                            OPERACIONES
 PRODUCTOS                              PRODUCTOS_BASE
 PRODUCTOS_UDF_RECARGAS                 PROMOCIONES_POR_CANTIDAD
 PROV                                   SCHEMA_INFO
 TURNOS                                 USUARIOS
 VENTAS                                 VENTATICKETS
 VENTATICKETS_ARTICULOS                 VENTA_DE_RECARGAS
'''
'''
PRODUCTOS_COLUMNS:
[('CHECADO_EN                     ',), ('CODIGO                         ',), ('DESCRIPCION                    ',), ('TVENTA                         ',), ('PCOSTO                         ',), ('PVENTA                         ',), ('DEPT
                          ',), ('PROVID                         ',), ('UMEDIDA                        ',), ('MAYOREO
                      ',), ('IPRIORIDAD                     ',), ('DINVENTARIO                    ',), ('DINVMINIMO
                  ',), ('DINVMAXIMO                     ',), ('PORCENTAJE_GANANCIA            ',), ('COMPONENTES
              ',), ('IMPUESTOS                      ',), ('PVENTA_ANTERIOR                ',), ('PCOSTO_ANTERIOR
          ',), ('PMAYOREO_ANTERIOR              ',)]
'''
'''
DEPT:
0 = []
1 = []
2 = SIN DEPT
3 = SIN DEPT
4 = []
5 = []
6 = BIMBO BLANCO
7 = BIMBO DULCE
8 = BARCEL
9 = SABRITAS
10 = LEO
11 = ENCANTO
12 = BOKADOS
13 = MARINELA PASTEL
14 = RICOLINO
15 = LALA
16 = COCA COLA
17 = PEPSI
18 = BONAFONT
31 = PALL MALL
'''

'''
DEPARTAMENTOS [ID, NOMBRE, PORCENTAJE_IMPUESTO, ACTIVO]
[(3, '- Sin Departamento -', 0, '1'), (2, 'Sin Departamento', 0, '1'), (5, 'Productos Comunes', 0, '0'), (6, 'Bimbo Blanco', 0, '1'), (7, 'Bimbo Dulce ', 0, '1'), (8, 'Barcel', 0, '1'), (9, 'Sabritas', 0, '1'), (10, 'Leo', 0, '1'), (11, 'Encanto', 0, '1'), (12, 'Bokados', 0, '1'), (13, 'Marinela Pastel', 0, '1'), (14, 'Ricolino', 0, '1'), (15, 'Lala',
0, '1'), (16, 'Coca-Cola', 0, '1'), (17, 'Pepsi', 0, '1'), (18, 'Bonafont Botella', 0, '1'), (19, 'bonafon garrafon (Eliminado 08/12/2022)', 0, '0'), (20, 'Peñafiel', 0, '1'), (21, 'valle (Eliminado 08/12/2022)', 0, '0'), (22, 'Gamesa', 0, '1'), (23, 'Treviño', 0, '1'), (24, 'tang (Eliminado 08/12/2022)', 0, '0'), (25, 'Tía Rosa', 0, '1'), (26, 'Tostitos', 0, '1'), (27, 'Sigma', 0, '1'), (28, 'Verdura', 0, '1'), (29, '59 (Eliminado 08/12/2022)', 0, '0'), (30, 'Del Valle', 0, '1'), (31, 'Pall Mall', 0, '1'), (32, 'Bonafont Garrafon', 0, '1'), (33, 'Varios', 0, '1'), (34, 'Bimbo Totopos', 0, '1'), (35, 'Marinela Galleta', 0, '1'), (36, 'Tostadas Norteñas', 0, '1')]
'''