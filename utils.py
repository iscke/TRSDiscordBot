'''
Takes a message that is formatted like a command.
Returns a list of each individual argument. 
The first argument is split by a FIRST_SEPARATOR (default space) - the rest are split by SEPARATOR (default comma).

Example: send user, hello, final
RETURNS: ['send','user','hello','final']

Parameters:
strip - Strips each parameter of surrounding spaces.
separator - character separating arguments.
first_separator - character separating the first argument and the rest.

This is a simplified version of argParse that doesn't use:
 - keyword arguments (e.g. rolls=5)
 - escaping (e.g. a backslash before a comma to show it is the same argument)
 - quotations to denote text as not containing special characters
If these are necessary it can be upgraded easily by changing this function.
'''

def argParse(message, strip=True, separator=',', first_separator=' '):
    arguments = message.split(first_separator, maxsplit=1)

    #arguments present
    if len(arguments) > 1:
        if strip:
            arguments = [arguments[0]] + [i.strip() for i in arguments[1].split(separator)]
        else:
            arguments = [arguments[0]] + arguments[1].split(separator)

    #no arguments present
    else:
        if strip:
            arguments[0].strip()

    return arguments
