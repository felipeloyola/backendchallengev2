import re

class Param(object):
    def __init__(self, key, value, required=True, re=None):
        super(Param, self).__init__()
        self.key = key
        self.value = value
        self.required = required
        self.re = re

    def valid(self):
        is_none_or_empty = self.value is None or len(self.value) == 0
        is_re_valid = self.re is None or (re.match(self.re, self.value) is not None)
        return self.required and not is_none_or_empty and is_re_valid

class ParameterManager(object):

    def __init__(self, app):
        super(ParameterManager, self).__init__()
        self.app = app
        self.params = dict()
        self.is_valid = True

    def add(self, key, value=None, required=True, re=None):
        
        if key in self.params:
            self.params[key].value = value
        else:
            param = Param(key, value, required, re)
            self.params[key] = param
            
    def load(self, a_dict):
        for key, value in a_dict.items():
            self.add(key, value)

    def get_params(self):
        params = dict()
        for param in self.params.values():
            params[param.key] = param.value
        return params

    def get(self, key):
        return self.params.get(key).value

    def has_params(self):
        return len(self.params)

    def valid(self):
        for param in self.params.values():
            if not param.valid():
                self.app.logger.warning(f"param {param.key} not valid", f"value {param.value}")
                return False
        return True


        