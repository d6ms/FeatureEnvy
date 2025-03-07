package gr.uom.java.distance;

import gr.uom.java.ast.MethodObject;
import gr.uom.java.ast.decomposition.AbstractStatement;

import java.util.*;

public class MyMethod extends Entity {

    private String classOrigin;
    private String methodName;
    private String packageName;
    private String returnType;
    private List<String> parameterList;
    private MyMethodBody methodBody;
    private boolean isAbstract;
    private String access;
    private MethodObject methodObject;
    private volatile int hashCode = 0;
    private Set<String> newEntitySet;

    public MyMethod(String classOrigin, String methodName, String packageName, String returnType, List<String> parameterList) {
        this.classOrigin = classOrigin;
        this.methodName = methodName;
        this.packageName = packageName;
        this.returnType = returnType;
        this.parameterList = parameterList;
        this.isAbstract = false;
        this.newEntitySet = null;
    }

    public void setMethodObject(MethodObject methodObject) {
    	this.methodObject = methodObject;
    }

    public MethodObject getMethodObject() {
    	return this.methodObject;
    }

    public String getAccess() {
        return access;
    }

    public void setAccess(String access) {
        this.access = access;
    }

    public void setMethodBody(MyMethodBody methodBody) {
    	this.methodBody = methodBody;
    }

    public MyMethodInvocation generateMethodInvocation() {
        return new MyMethodInvocation(this.classOrigin,this.methodName,this.returnType,this.parameterList);
    }

    public boolean isAbstract() {
        return isAbstract;
    }

    public void setAbstract(boolean anAbstract) {
        isAbstract = anAbstract;
    }

    public boolean containsParameter(String p) {
        for(String parameter : parameterList) {
            if(parameter.equals(p))
                return true;
        }
        return false;
    }

    public void setClassOrigin(String className) {
        this.classOrigin = className;
    }

    public void removeParameter(String className) {
        this.parameterList.remove(className);
    }

    public void addParameter(String parameter) {
        if(!parameterList.contains(parameter))
            parameterList.add(parameter);
    }

    public String getClassOrigin() {
        return classOrigin;
    }

    public String getMethodName() {
        return methodName;
    }
    
    public String getPackageName() {
    	return packageName;
    }

    public void setMethodName(String methodName) {
		this.methodName = methodName;
	}

	public String getReturnType() {
        return returnType;
    }

    public List<String> getParameterList() {
        return parameterList;
    }

    public void replaceMethodInvocationsWithAttributeInstructions(Map<MyMethodInvocation, MyAttributeInstruction> map) {
        if(this.methodBody != null)
        	this.methodBody.replaceMethodInvocationsWithAttributeInstructions(map);
    }

    public void replaceMethodInvocation(MyMethodInvocation oldMethodInvocation, MyMethodInvocation newMethodInvocation) {
    	if(newEntitySet != null) {
    		if(newEntitySet.contains(oldMethodInvocation.toString())) {
    			newEntitySet.remove(oldMethodInvocation.toString());
        		newEntitySet.add(newMethodInvocation.toString());
    		}
    	}
    	else {
	    	if(this.methodBody != null)
	    		this.methodBody.replaceMethodInvocation(oldMethodInvocation, newMethodInvocation);
    	}
    }

    public void replaceAttributeInstruction(MyAttributeInstruction oldInstruction, MyAttributeInstruction newInstruction) {
    	if(newEntitySet != null) {
    		if(newEntitySet.contains(oldInstruction.toString())) {
    			newEntitySet.remove(oldInstruction.toString());
        		newEntitySet.add(newInstruction.toString());
    		}
    	}
    	else {
    		if(this.methodBody != null)
    			this.methodBody.replaceAttributeInstruction(oldInstruction, newInstruction);
    	}
    }

    public void removeAttributeInstruction(MyAttributeInstruction attributeInstruction) {
    	if(newEntitySet != null) {
    		newEntitySet.remove(attributeInstruction.toString());
    	}
    	else {
    		if(this.methodBody != null)
    			this.methodBody.removeAttributeInstruction(attributeInstruction);
    	}
    }

    public void setAttributeInstructionReference(MyAttributeInstruction myAttributeInstruction, boolean reference) {
    	if(this.methodBody != null)
    		this.methodBody.setAttributeInstructionReference(myAttributeInstruction, reference);
    }

    public void addAttributeInstructionInStatementsOrExpressionsContainingMethodInvocation(MyAttributeInstruction attributeInstruction, MyMethodInvocation methodInvocation) {
    	if(newEntitySet != null) {
    		if(newEntitySet.contains(methodInvocation.toString()) && !attributeInstruction.isReference())
    			newEntitySet.add(attributeInstruction.toString());
    	}
    	else {
	    	if(this.methodBody != null) {
	    		this.methodBody.addAttributeInstructionInStatementsOrExpressionsContainingMethodInvocation(attributeInstruction, methodInvocation);
	    	}
    	}
    }

    public void insertMethodInvocationBeforeStatement(MyAbstractStatement parentStatement, MyStatement methodInvocation) {
    	if(this.methodBody != null)
    		this.methodBody.insertMethodInvocationBeforeStatement(parentStatement, methodInvocation);
    }

    public void removeStatement(MyAbstractStatement statementToRemove) {
    	if(this.methodBody != null)
    		this.methodBody.removeStatement(statementToRemove);
    }

    public void replaceSiblingStatementsWithMethodInvocation(List<MyAbstractStatement> statementsToRemove, MyStatement methodInvocation) {
		if(this.methodBody != null)
			this.methodBody.replaceSiblingStatementsWithMethodInvocation(statementsToRemove, methodInvocation);
	}

    public MyAbstractStatement getAbstractStatement(AbstractStatement statement) {
    	if(this.methodBody != null)
    		return this.methodBody.getAbstractStatement(statement);
    	else
    		return null;
    }

    public ListIterator<MyMethodInvocation> getMethodInvocationIterator() {
    	if(this.methodBody != null)
    		return this.methodBody.getMethodInvocationIterator();
    	else
    		return new ArrayList<MyMethodInvocation>().listIterator();
    }

    public ListIterator<MyAttributeInstruction> getAttributeInstructionIterator() {
    	if(this.methodBody != null)
    		return this.methodBody.getAttributeInstructionIterator();
    	else
    		return new ArrayList<MyAttributeInstruction>().listIterator();
    }

	public boolean containsAttributeInstruction(MyAttributeInstruction instruction) {
		if(newEntitySet != null) {
			return newEntitySet.contains(instruction.toString());
		}
		else {
			if(this.methodBody != null)
				return this.methodBody.containsAttributeInstruction(instruction);
			else
				return false;
		}
	}

	public boolean containsMethodInvocation(MyMethodInvocation invocation) {
		if(newEntitySet != null) {
			return newEntitySet.contains(invocation.toString());
		}
		else {
			if(this.methodBody != null)
				return this.methodBody.containsMethodInvocation(invocation);
			else
				return false;
		}
	}

    public int getNumberOfAttributeInstructions() {
    	if(this.methodBody != null)
    		return this.methodBody.getNumberOfAttributeInstructions();
    	else
    		return 0;
    }

    public int getNumberOfMethodInvocations() {
    	if(this.methodBody != null)
    		return this.methodBody.getNumberOfMethodInvocations();
    	else return 0;
    }

    public int getNumberOfParameters() {
        return this.parameterList.size();
    }

    public boolean equals(MyMethodInvocation methodInvocation) {
        return this.classOrigin.equals(methodInvocation.getClassOrigin()) &&
            this.methodName.equals(methodInvocation.getMethodName()) &&
            this.returnType.equals(methodInvocation.getReturnType()) &&
            this.parameterList.equals(methodInvocation.getParameterList());
    }

    public boolean equals(Object o) {
        if(this == o) {
            return true;
        }

        if (o instanceof MyMethod) {
            MyMethod method = (MyMethod)o;
            return this.classOrigin.equals(method.classOrigin) &&
                this.methodName.equals(method.methodName) &&
                this.returnType.equals(method.returnType) &&
                this.parameterList.equals(method.parameterList);
        }
        return false;
    }

    public int hashCode() {
    	if(hashCode == 0) {
    		int result = 17;
    		result = 37*result + classOrigin.hashCode();
    		result = 37*result + methodName.hashCode();
    		result = 37*result + returnType.hashCode();
    		for(String parameter : parameterList) {
    			result = 37*result + parameter.hashCode();
    		}
    		hashCode = result;
    	}
    	return hashCode;
    }

    public String toString() {
        StringBuilder sb = new StringBuilder();
        if(!classOrigin.equals(methodName))
            sb.append(classOrigin).append("::");
        sb.append(methodName);
        sb.append("(");
        if(!parameterList.isEmpty()) {
            for(int i=0; i<parameterList.size()-1; i++)
                sb.append(parameterList.get(i)).append(", ");
            sb.append(parameterList.get(parameterList.size()-1));
        }
        sb.append(")");
        if(returnType != null)
            sb.append(":").append(returnType);
        return sb.toString();
    }

    public Set<String> getEntitySet() {
    	Set<String> set = new HashSet<String>();
        ListIterator<MyAttributeInstruction> attributeInstructionIterator = getAttributeInstructionIterator();
        while(attributeInstructionIterator.hasNext()) {
        	MyAttributeInstruction attributeInstruction = attributeInstructionIterator.next();
            if(!attributeInstruction.isReference())
                set.add(attributeInstruction.toString());
        }
        ListIterator<MyMethodInvocation> methodInvocationIterator = getMethodInvocationIterator();
        while(methodInvocationIterator.hasNext()) {
        	MyMethodInvocation methodInvocation = methodInvocationIterator.next();
            if(!this.equals(methodInvocation))
            	set.add(methodInvocation.toString());
        }
        return set;
    }

    public static MyMethod newInstance(MyMethod method) {
        List<String> newParameterList = new ArrayList<String>();
        for(String parameter : method.parameterList)
            newParameterList.add(parameter);
        MyMethod newMethod = new MyMethod(method.classOrigin,method.methodName,method.packageName,method.returnType,newParameterList);
        if(method.isAbstract)
            newMethod.setAbstract(true);
        if(method.methodBody != null) {
        	MyMethodBody newMethodBody = MyMethodBody.newInstance(method.methodBody);
        	newMethod.setMethodBody(newMethodBody);
        }
        return newMethod;
    }

    public void initializeNewEntitySet() {
    	if(newEntitySet == null)
    		this.newEntitySet = getEntitySet();
    }

    public void resetNewEntitySet() {
    	this.newEntitySet = null;
    }

    public Set<String> getNewEntitySet() {
    	return this.newEntitySet;
    }

	public Set<String> getFullEntitySet() {
		Set<String> set = new HashSet<String>();
		set.add(this.toString());
        ListIterator<MyAttributeInstruction> attributeInstructionIterator = getAttributeInstructionIterator();
        while(attributeInstructionIterator.hasNext()) {
        	MyAttributeInstruction attributeInstruction = attributeInstructionIterator.next();
            set.add(attributeInstruction.toString());
        }
        ListIterator<MyMethodInvocation> methodInvocationIterator = getMethodInvocationIterator();
        while(methodInvocationIterator.hasNext()) {
        	MyMethodInvocation methodInvocation = methodInvocationIterator.next();
            set.add(methodInvocation.toString());
        }
        return set;
	}
}
