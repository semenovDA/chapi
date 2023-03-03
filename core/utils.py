from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    # if response is not None:
    #     response.data = None
    
    return response

def ValidateDict(data):
    for v in data.values():

        if(v == None):
            return False

        if(type(v) != list and type(v) != str):
            if(v <= 0):
                return False

        elif(type(v) == list):
            for i in v:
                if(i == None):
                    return False
                if(i <= 0):
                    return False        
        
        elif(type(v) == str):
            if v == '':
                return False

    return True