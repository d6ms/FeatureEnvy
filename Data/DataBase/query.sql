select l.methodName, cs.package_name as src_package, cd.package_name as dst_package, l.src_distance, l.dst_distance
from rel2 l
inner join classinfo cs on l.src_class = cs.ClassQualifiedName 
inner join classinfo cd on l.dst_class = cd.ClassQualifiedName 
where cs.package_name != cd.package_name ;
