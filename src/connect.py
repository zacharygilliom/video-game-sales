import sqlite3
import pandas as pd

class VideoGameSales:

    def __init__(self, path):
        self.path = path

    def connectToDatabase(self):
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM sales")
        rows = cur.fetchall()
        return rows

    def makeDataframe(self):
        rows = self.connectToDatabase()
        cols = ['Rank', 'Name', 'Platform', 'Year', 'Genre', 'Publisher', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']
        self.df = pd.DataFrame(columns=cols, data=rows)
        print(self.df.head())

    def cleanDataframe(self):
        self.df = self.df.astype({'NA_Sales': 'float64', 'EU_Sales':'float64', 'JP_Sales':'float64', 'Other_Sales':'float64', 'Global_Sales':'float64'})

    def byYearDataframe(self):
        df = self.df
        df = df.astype({'NA_Sales': 'float64', 'EU_Sales':'float64', 'JP_Sales':'float64', 'Other_Sales':'float64', 'Global_Sales':'float64'})
        df = df.groupby(by=['Year']).mean()
        df.reset_index(inplace=True)
        return df

    def meltDataframe(self, df):
        df= df.melt(id_vars=['Year'], value_vars=['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales'], var_name='Sales_Region', value_name='Total_Sales')
        return df

    def topThreePlatoformsByYearAndRegion(self, salesRegion):
        df = self.df
        df = df.astype({'NA_Sales': 'float64', 'EU_Sales':'float64', 'JP_Sales':'float64', 'Other_Sales':'float64', 'Global_Sales':'float64'})
        df = df.groupby(by=['Year', 'Platform']).sum()
        df = df[salesRegion].groupby('Year', group_keys=False).nlargest(3)
        #df = df.nlargest(10,columns=['NA_Sales'])
        df = df.reset_index()
        print(df.head(30))
        return df
 