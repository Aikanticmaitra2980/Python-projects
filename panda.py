import numpy as np
import pandas as pd

data={"Name":["Aikantic Maitra","Swastik Basak","Arkadeep Chakraborty","Rohan Das"],
      "MarksObtaned":["54","70","45","65"]
      }
df=pd.DataFrame(data)
stats=df.describe()
stats.to_excel("marks.xlsx")
print(df)
df.to_csv("marks.csv",index=False)

