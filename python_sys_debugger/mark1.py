import sys
print(sys.ps1)

def trace_calls(frame,event,args) : 
	if(event == 'call') : 
		print(frame.f_code.co_name)
		print(frame.f_lineno)

def a() : 
	print('in a()') 
def b() : 
	print('in b()')
	a()

sys.settrace(trace_calls)
b()