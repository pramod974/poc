import pandas as pd
import numpy as np
df = pd.read_csv("/Users/pramodkumar/Downloads/poc/Finocracy/CustomerRetention.csv")
df.head()
df.dtypes
obj_df = df.select_dtypes(include=['object']).copy()
obj_df[obj_df.isnull().any(axis=1)]
cleanup_nums = {"gender":{"Female": 1, "Male": 0},
                "Partner": {"Yes": 1, "No": 0},
                "Dependents":{"Yes":1,"No":0},
                "DigitalBanking":{"Yes":1,"No":0},
                "MultipleDigitalServices":{"No digital service":2,"Yes":1,"No":0},
                "OnlineService":{"s1":1,"s2":1,"No":0},
                "ShareTrade":{"No online service":2,"Yes":1,"No":0},
                "Loan":{"No online service":2,"Yes":1,"No":0},
                "Deposits":{"No online service":2,"Yes":1,"No":0},
                "TechSupport":{"No online service":2,"Yes":1,"No":0},
                "DebitCard":{"No online service":2,"Yes":1,"No":0},
                "CreditCard":{"No online service":2,"Yes":1,"No":0},
                "Contract":{"Two year":2,"One year":1,"Month-to-month":0},
                "PaperlessStatement":{"Yes":1,"No":0},
                "PaymentMethod":{"Electronic check":0,"Mailed check":1,"Bank transfer (automatic)":2,"Credit card (automatic)":3},
                "Churn":{"Yes":1,"No":0}
                }
obj_df.replace(cleanup_nums, inplace=True)
obj_df.head()