class debugger() : 
	def __init__(self,function) : 
		self.function = function

	def __call__(self,*args,**kwargs) :
		print('entering ',self.function.__name__)
		self.function(args,kwargs)
		print('exiting ',self.function.__name__)

# @debugger
# def add(a,b) : 
# 	return(a+b)

# add(2,3)