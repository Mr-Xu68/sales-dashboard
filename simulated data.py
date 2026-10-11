from builtins import print

import pandas as pd
import numpy as np

#设置随机种子
np.random.seed(42)
num_records = 100

products=['产品A','产品B','产品C','产品D']
regions=['区域A','区域B','区域C','区域D']

#设置随机时间
data = pd.date_range(start='2022-01-01',periods=num_records,freq='D')
product = np.random.choice(products,num_records)
region = np.random.choice(regions,num_records)
sales = np.random.randint(100,1000,num_records)
price = np.random.randint(10,100,num_records)

df = pd.DataFrame({
    '日期':data,
    '产品':product,
    '区域':region,
    '销售量':sales,
    '单价':price,
    '销售额':sales*price,
})
df.to_csv('sales_data.csv',index=False)