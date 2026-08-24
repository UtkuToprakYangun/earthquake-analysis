#Importing Libraries
import requests 
import pandas as pd 

#Fetching Data from the Internet
url = "http://www.koeri.boun.edu.tr/scripts/lst4.asp"
response = requests.get(url) 
response.encoding = "windows-1254"

#Extracting the Relevant Text Block
start = response.text.find("<pre")
end = response.text.find("</pre>")
raw_data = response.text[start:end]

#Splitting the Text into Lines and Cleaning the Headers
lines = raw_data.split("\n")
data_lines = lines[7:]
data_lines = [line for line in data_lines if line.strip() != ""] #delete empty line

#Line Parsing Function
def parse_line(line):
    parts = line.split()
    location = " ".join(parts[8:-1]) #Because there are spaces between the location data
    earthquake = {
        "day": parts[0],
        "time": parts[1],
        "latitude": parts[2],
        "longitude": parts[3],
        "depth": parts[4],
        "MD": parts[5],
        "ML": parts[6],
        "Mw": parts[7],
        "location": location,
        "type": parts[-1]
    }
    return earthquake

#Processing All Data
earthquakes = []
for line in data_lines :
    result = parse_line(line)
    earthquakes.append(result)

#Creating the DataFrame and Correcting Data Types
df = pd.DataFrame(earthquakes)
df["latitude"] = df["latitude"].astype(float)
df["longitude"] = df["longitude"].astype(float)
df["depth"] = df["depth"].astype(float)
df["ML"] = df["ML"].astype(float)

df["MD"] = df["MD"].replace("-.-",float("nan"))
df["Mw"] = df["Mw"].replace("-.-",float("nan"))
df["MD"] = df["MD"].astype(float)
df["Mw"] =df["Mw"].astype(float)

#convert type to day and time
df["day"] = pd.to_datetime(df["day"], format = "%Y.%m.%d")
df["time"] = pd.to_datetime(df["time"],format= "%H:%M:%S").dt.time

df.to_csv("data/earthquakes.csv", index = False)

df2 = pd.read_csv("data/earthquakes.csv")
print(df2.shape)