
# dump.dump(self.response, ['request', '_request', 'response', 'object', '__path__', 'selected_objects', 'single_object', 'session', '_raw_session', 'css', 'styles' , 'language_dirs', 'language_dict', 'user'])

default_exclude = ['request', 'response', 'obj', 'cobj', 'css', '__action_roles__', '__path__', '__ws_group__',  '__obj_set__', '_request', '__pref__']

import os
os.environ['DUMP_FILE'] = 'dump.log'

pos = 0

def put(*vals):
	putI(0, *vals)

def line(*vals):
	lineI(0, *vals)

def tab(indent):
	global pos
	if indent == 0:
		pass
	elif indent > 0:
		putI(0, (indent-1)*' ')
	elif pos == 0:
		tab(-indent)

def putI(indent, *vals):
	global pos
	tab(indent)
	for val in [str(v) for v in vals]:
		_write(val)
		_write(' ')
		pos += len(val)+1

def lineI(indent, *vals):
	global pos
	putI(indent, *vals)
	_new_line()
	pos = 0

def error(_raise = 0) :
	import sys
	exc_type  = sys.exc_type
	exc_value = sys.exc_value
	try :
		_new_line()
		global logF
		import traceback
		_open()
		traceback.print_exc(None, logF)
		_new_line()
	finally :
		_close()
	if _raise : raise exc_type, exc_value

def single_value(val):
	if len(val) == 0:
		return True
	elif len(val) == 1:
		return not (type(val[0]) in [list, tuple, dict] or hasattr(val[0], '__dict__'))
	else:
		return False

def dump(val, exclude=default_exclude, indent=0, objs=[]):
	from types import ModuleType, InstanceType
	if type(val) == list:
		if single_value(val):
			lineI(-indent, repr(val))
		else:
			lineI(-indent, '[')
			for v in val: dump(v, exclude, indent+2, objs)
			lineI(-indent, ']')
	elif type(val) == tuple:
		if single_value(val):
			lineI(-indent, repr(val))
		else:
			lineI(-indent, '(')
			for v in val: dump(v, exclude, indent+2, objs)
			lineI(-indent, ')')
	elif type(val) in [int, str, long, bool]:
		lineI(-indent, repr(val))
	elif type(val) == ModuleType:
		lineI(-indent, type(val), repr(val))
	elif isinstance(val, dict): # type(val) == dict:
		lineI(-indent, '{')
		indent += 2
		items = val.items()
		items.sort()
		for k,v in items:
			putI(-indent, repr(k).ljust(11) + ':')
			if k in ['__builtins__']:
				lineI(0, '{...}')
			elif k in exclude:
				lineI(0, type(val), repr(v))
			elif type(v) in [list, tuple] and single_value(v):
				dump(v, exclude, indent, objs)
			elif type(v) in [list, tuple] or isinstance(v, dict) or hasattr(v, '__dict__'):
				dump(v, exclude, indent+13, objs)
			else:
				dump(v, exclude, indent, objs)
		indent -= 2
		lineI(-indent, '}')
	elif hasattr(val, '__dict__'):
		cl = getattr(val, '__class__', None)
		if cl : cl = val.__class__.__name__
		repr_val = (cl != 'Response') and repr(val) or ''
		putI(-indent, type(val), repr_val, )
		dump_instance = type(val) is InstanceType
		if not dump_instance and val not in objs:
			objs.append(val)
			dump_instance = True
		if dump_instance:
			dump(val.__dict__, exclude, indent, objs)
		else:
			lineI(0, '')
	else:
		lineI(-indent, type(val), repr(val))

def clear():
	_clear()


#-----------------------------------------------------------------------

_nl = 0
_closed = 1
_stdout = 0

def _new_line():
	global _nl
	_write("\n")
	_close()
	_nl = 1

def _open():
	global logF, _closed, _stdout
	import os, sys
	dump_file = os.environ.get('DUMP_FILE')
	if dump_file:
		logF = open(dump_file, "a")
		_stdout = 0
	else:
		logF = sys.stdout
		_stdout = 1
	_closed = 0

def _clear():
	global logF, _closed
	import os, sys
	dump_file = os.environ.get('DUMP_FILE')
	if dump_file:
		logF = open(dump_file, "w")
		_close()
		_closed = 0

def _write(value):
	global logF, _nl, _closed
	if _closed :
		_open()
	if _nl :
		_nl = 0
	logF.write(value)

def _close():
	global logF, _closed
	if not _closed and not _stdout:
		logF.close()
		_closed = 1
