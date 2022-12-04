class Error:
    def error(self,error):
        error_dict = {}
        for key, value in error.items():
            error_dict["errors"] = value
        return error_dict

class Success:
    def success(self,success):
        success_dict = {}
        for key, value in success.items():
            success_dict["success"] = value
        return success_dict

