import inspect

# Logger for logging messages to the user
class Logger:
    # Logs an error to the console.
    # Prints the name of the function where it came from, if show_func_name = True.
    def log_error(msg, show_func_name = False):
        if Logger.log_level >= 2:
            if show_func_name:
                print('ERROR in ', inspect.stack()[1][3], '(): ', msg, sep='')
            else:
                print('ERROR:', msg)
    
    # Logs a warning to the console.
    # Prints the name of the function where it came from, if show_func_name = True.
    def log_warning(msg, show_func_name = False):
        if Logger.log_level >= 1:
            if show_func_name:
                print('WARNING in ', inspect.stack()[1][3], '(): ', msg, sep='')
            else:
                print('WARNING:', msg)

    # Logs info to the console.
    # Prints the name of the function where it came from, if show_func_name = True.
    def log_info(msg, show_func_name = False):
        if Logger.log_level >= 0:
            if show_func_name:
                print('INFO in ', inspect.stack()[1][3], '(): ', msg, sep='')
            else:
                print('INFO:', msg)

    # Level of verbosity of the the logger
    # On level 0 only info messages are printed
    # On level 1 info and warning messages are printed
    # On level 2 info, warning and error messages are printed
    log_level = 2