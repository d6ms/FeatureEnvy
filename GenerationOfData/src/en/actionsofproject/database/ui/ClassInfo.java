package en.actionsofproject.database.ui;

public class ClassInfo {
	int ClassID;
	String ClassQualifiedName;
	String ClassName;
	String packageName;
	
	public ClassInfo(int ClassID, String ClassQualifiedName, String ClassName, String packageName){
		this.ClassID = ClassID;
		this.ClassQualifiedName = ClassQualifiedName;
		this.ClassName = ClassName;
		this.packageName = packageName;
	}
	public int getClassID() {
		return ClassID;
	}
	
	public String getClassName() {
		return ClassName;
	}
	public String getPackageName() {
		return packageName;
	}
	public void setClassName(String className) {
		ClassName = className;
	}
	public void setClassID(int classID) {
		ClassID = classID;
	}
	public String getClassQualifiedName() {
		return ClassQualifiedName;
	}

	public void setClassQualifiedName(String classQualifiedName) {
		ClassQualifiedName = classQualifiedName;
	}

}
