
import pandas as pd
import base64


class functions:
    def __init__(self, conf_file, data):
        with open(conf_file, 'r') as f:
            self.conf_file = json.load(f)
        self.data = pd.read_csv(data)
     
  
    def encode_image(image_file):
        ''' 
        Function to encode a image in a format that allows its plot on html.Fig
        '''
        encode = base64.b64encode(open(image_file, "rb").read())
        return "data:image/jpeg;base64,{}".format(encode.decode())

 






    


    

    
