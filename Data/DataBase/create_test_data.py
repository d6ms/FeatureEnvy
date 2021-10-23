import os
import sys
import mysql.connector as mydb
from collections import namedtuple
from itertools import groupby

METHOD_LENGTH = 5
PACKAGE_LENGTH = 5

conn = mydb.connect(
    host='127.0.0.1',
    port='3306',
    user='root',
    password='12345',
    database='testdata'
)

project = sys.argv[1] # jsmoothgen, xdman, neuroph-core
if not project:
    raise Error('specify target project')

output_dir = f'../test/{project}'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

query = f'''
select l.MethodId, l.methodName, cs.package_name as src_package, cd.package_name as dst_package, l.src_distance, l.dst_distance
from rel2 l
inner join classinfo cs on l.src_class = cs.ClassQualifiedName 
inner join classinfo cd on l.dst_class = cd.ClassQualifiedName 
where cs.package_name != cd.package_name 
and cs.project_name = '{project}'
order by l.MethodId ;
'''


DataRow = namedtuple('DataRow', [
    'methodId',
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
    if len(splitted) >= PACKAGE_LENGTH:
        splitted = splitted[-PACKAGE_LENGTH:]
    else:
        splitted = ['*'] * (PACKAGE_LENGTH - len(splitted)) + splitted
    return splitted

def main():
    cur = conn.cursor()
    cur.execute(f'''
    select distinct(package_name)
    from classinfo 
    where project_name = '{project}';
    ''')
    rows = cur.fetchall()
    packages = [row[0] for row in rows]

    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    rows = [DataRow(*row) for row in rows]
    method_ids, method_names = [], []
    for method_id, rows in groupby(rows, key=lambda row: row.methodId):
        method_ids.append(method_id)
        f_name = open(f'{output_dir}/test_Names{method_id}.txt', mode='w')
        f_dist = open(f'{output_dir}/test_Distances{method_id}.txt', mode='w')
        seen = set()
        for i, row in enumerate(rows):
            if i == 0:
                name = ' '.join(split_package_name(row.sourcePackage))
                f_name.write(name + '\n')
                f_dist.write(str(row.sourceDistance) + '\n')
            name = ' '.join(split_package_name(row.targetPackage))
            f_name.write(name + '\n')
            f_dist.write(str(row.targetDistance) + '\n')
            seen.add(row.targetPackage)
        seen.add(row.sourcePackage)
        name = ' '.join(split_method_name(row.methodName))
        method_names.append(name)
        
        for package in packages:
            if package in seen:
                continue
            name = ' '.join(split_package_name(package))
            f_name.write(name + '\n')
            f_dist.write('1.0\n')

        f_name.close()
        f_dist.close()

    with open(f'{output_dir}/test_MethodId.txt', mode='w') as f:
        for method_id in method_ids:
            f.write(str(method_id) + ' 0\n')
    
    with open(f'{output_dir}/test_MethodNames.txt', mode='w') as f:
        for method_name in method_names:
            f.write(method_name + '\n')
       

main()
