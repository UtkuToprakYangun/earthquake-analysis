import pandas as pd

df = pd.read_csv("data/earthquakes.csv")

def extract_region(location) :
    
    paren_index = location.find("(")
    if paren_index == -1 :
        return location
    else:   
        region= location[paren_index:]
        region = region.strip("()")
        return region

df["region"] = df["location"].apply(extract_region)
earth_count = df.groupby("region")["ML"].count().sort_values(ascending=False)

biggest_earthquake = df.sort_values("ML", ascending=False).head(10)
print(biggest_earthquake)