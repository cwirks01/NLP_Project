import pandas as pd
import json

json_file = {"chase": ["car", "mortorcycle"],
             "sam": "juke",
             "car": "chase",
             "motorcycle": "chase",
             "juke": "sam"}

test_text = ["chase", "juke"]

t=pd.DataFrame(json_file,)
