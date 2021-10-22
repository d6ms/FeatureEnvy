import mysql.connector as mydb
from collections import namedtuple

METHOD_LENGTH = 5
PACKAGE_LENGTH = 5

conn = mydb.connect(
    host='127.0.0.1',
    port='3306',
    user='root',
    password='12345',
    database='testdata'
)


with open('query.sql', mode='r') as f:
    query = ''.join(f.readlines())


DataRow = namedtuple('DataRow', [
    'methodName', 
    'sourcePackage',
    'targetPackage',
    'sourceDistance', 
    'targetDistance'
])

def split_method_name(methodName):
    splitted = []

    if '_' in methodName:
        for part in methodName.split('_'):
            splitted.extend(split_method_name(part))
    else:
        buf = ''
        for i, c in enumerate(methodName):
            if i == 0:
                buf += c.lower()
                continue
            if c.lower() != c or c.isnumeric():
                splitted.append(buf)
                buf = c.lower()
            else:
                buf += c.lower()
        if buf:
            splitted.append(buf)
        
    splitted = splitted[:METHOD_LENGTH]
    if len(splitted) < METHOD_LENGTH:
        splitted = ['*'] * (METHOD_LENGTH - len(splitted)) + splitted
    return splitted

def split_package_name(packageName):
    splitted = packageName.split('.')
    splitted = [name.lower() for name in splitted]
    splitted = splitted[:PACKAGE_LENGTH]
    if len(splitted) < PACKAGE_LENGTH:
        splitted = ['*'] * (PACKAGE_LENGTH - len(splitted)) + splitted
    return splitted

def main():
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()

    f_names = open('train_Names.txt', mode='w')
    f_distances = open('train_Distances.txt', mode='w')
    try:
        for row in rows:
            row = DataRow(*row)
            methodName = split_method_name(row.methodName)
            sourcePackage = split_package_name(row.sourcePackage)
            targetPackage = split_package_name(row.targetPackage)

            names0 = ' '.join(methodName + sourcePackage + targetPackage)
            names1 = ' '.join(methodName + targetPackage + sourcePackage)
            f_names.write(names0 + '\n')
            f_names.write(names1 + '\n')

            dist0 = f'{row.sourceDistance} {row.targetDistance} 0'
            dist1 = f'{row.targetDistance} {row.sourceDistance} 1'
            f_distances.write(dist0 + '\n')
            f_distances.write(dist1 + '\n')
    finally:
        f_names.close()
        f_distances.close()


main()
