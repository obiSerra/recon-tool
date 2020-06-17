class Logger():
    def __init__(self,filename, clean_file=True):
        self.filename = filename
        if clean_file:
            self.clean()
        
    def clean(self):
        open(self.filename, 'w').close() 
        
    def append_row(self, row):
        with open(self.filename, 'a+') as f:
            f.write(','.join([str(r) for r in row]) + '\n')
