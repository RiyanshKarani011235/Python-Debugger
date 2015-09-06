import os
os.chdir('/users/ironstein/documents/projects working directory/Python-Debugger')

from _ast import *

def parse(source,filename='<unknown>',mode='exec') : 
	return compile(source,filename,mode,PyCF_ONLY_AST)

class node_visitor() : 

	def iter_fields(self,node) : 
		for field in node._fields :
			try : 
				yield field,getattr(node,field)
			except AttributeError : 
				pass

	def visit(self,node) : 
		method = 'visit_' + node.__class__.__name__
		visitor_function = getattr(self,method,self.generic_visitor)
		return visitor_function(node)

	def generic_visitor(self,node) : 
		for field,value in self.iter_fields(node)  :
			if isinstance(value,AST) : 
				self.visit(value)
			elif isinstance(value,list) : 
				for element in value : 
					if isinstance(element,AST) : 
						self.visit(element)

class node_transformer(node_visitor) : 
	def generic_visitor(self,node) : 
		for field,old_node in self.iter_fields(node) :
			if isinstance(old_node,AST) : 
				new_node = self.visit(old_node)
				if new_node is None : 
					continue
				else : 
					setattr(node,field,new_node)

			elif isinstance(old_node,list) : 
				new_node = []
				for element in old_node : 
					if isinstance(element,AST) : 
						new_element = self.visit(element)
						if new_element is None :
							continue
						elif not isinstance(new_element,AST) : 
							new_node.extend(new_element)
							continue
					new_node.append(new_element)
				old_node[:] = new_node
			else : 
				print('terminal branch reached',end = ':')
				print(node.__class__.__name__)
				for field in node._fields : 
					print(field , ':',getattr(node,field),end = ', ')
				print()

class special_classes() : 
	class print_functions(node_transformer) :
		def visit_FunctionDef(self,node) :
			self.generic_visitor(node)


tree = parse('def sum(a,b) :\n\tc = a + b\n\treturn c')

tree1 = parse('testing',filename='/users/ironstein/documents/projects working directory/Python-Debuggertest_source')
# tree = parse("print('i am iron man')")
special_classes().print_functions().visit(tree)
print('----------------------------------------')
special_classes().print_functions().visit(tree1)

# node_transformer().visit(tree)

#tree1 = parse('testing',filename='/users/ironstein/documents/projects working directory/Python-Debuggertest_source')
#special_classes().print_functions().visit(tree1)

# node_transformer().visit(tree)
