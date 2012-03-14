def parseCommand(string):	
	argument = string.rsplit('-')
	if len(argument) > 3:
		print("Pare Error: Too many arguments")
		return(None, None, None)

	if len(argument) >0:	
		arg1 = argument[0].rstrip()
		arg1 = arg1.lstrip()
		arg1 = arg1.lower()
		if len(argument)==1:
			return (arg1, None , None)

	if len(argument) >1:
		arg2 = argument[1].rstrip()
		arg2 = arg2.lstrip()
		arg2 = arg2.lower()
		if len(argument)==2:
			return (arg1, arg2, None)
	
	if len(argument)  >2:
		arg3 = argument[2].rstrip()
		arg3 = arg3.lstrip()
		arg3 = arg3.lower()
		return (arg1, arg2, arg3)
		
	return (None, None, None)
		