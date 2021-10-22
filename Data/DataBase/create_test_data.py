import os
import sys
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

project = sys.argv[1] # jsmoothgen, xdman, neuroph-core
if not project:
    raise Error('specify target project')

output_dir = f'../test/{project}'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

query = f'''
select cs.ClassId, l.methodName, cs.package_name as src_package, cd.package_name as dst_package, l.src_distance, l.dst_distance
from rel2 l
inner join classinfo cs on l.src_class = cs.ClassQualifiedName 
inner join classinfo cd on l.dst_class = cd.ClassQualifiedName 
where cs.package_name != cd.package_name
and cs.project_name = '{project}'
order by cs.ClassId 
;
'''


DataRow = namedtuple('DataRow', [
    'classId',
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

    class_ids, names, distances = [], [], []
    for row in rows:
        row = DataRow(*row)
        if class_ids and class_ids[-1] != row.classId:
            with open(f'{output_dir}/test_Names{class_ids[-1]}.txt', mode='w') as f:
                for name in names:
                    f.write(name + '\n')
            with open(f'{output_dir}/test_Distances{class_ids[-1]}.txt', mode='w') as f:
                for distance in distances:
                    f.write(distance + '\n')
            names, distances = [], []
        
        if not class_ids or class_ids[-1] != row.classId:
            class_ids.append(row.classId)
    
        distances.append(f'{row.sourceDistance} {row.targetDistance} 0')

        methodName = split_method_name(row.methodName)
        sourcePackage = split_package_name(row.sourcePackage)
        targetPackage = split_package_name(row.targetPackage)
        names.append(' '.join(methodName + sourcePackage + targetPackage))
    
    with open(f'{output_dir}/test_Names{class_ids[-1]}.txt', mode='w') as f:
        for name in names:
            f.write(name + '\n')
    with open(f'{output_dir}/test_Distances{class_ids[-1]}.txt', mode='w') as f:
        for distance in distances:
            f.write(distance + '\n')
    with open(f'{output_dir}/test_ClassId.txt', mode='w') as f:
        for class_id in class_ids:
            f.write(str(class_id) + '\n')

main()
