import sqlite3
import pandas as pd

class VideoGameSales:

    def __init__(self, rows, cols):
        self.df = pd.DataFrame(columns=cols, data=rows).astype(dtype={'NA_Sales': 'float64', 'EU_Sales': 'float64', 'JP_Sales':'float64', 'Other_Sales': 'float64', 'Global_Sales': 'float64'})

    def byYearDataframe(self):
        df = self.df.groupby(by=['Year']).mean()
        df.reset_index(inplace=True)
        return df

    def meltDataframe(self):
        df = self.byYearDataframe() 
        df= df.melt(id_vars=['Year'], value_vars=['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales'], var_name='Sales_Region', value_name='Total_Sales')
        return df

    def topThreePlatoformsByYearAndRegion(self, salesRegion):
        df = self.df.groupby(by=['Year', 'Platform']).sum()
        df = df[salesRegion].groupby('Year', group_keys=False).nlargest(3)
        df = df.reset_index()
        return df
 