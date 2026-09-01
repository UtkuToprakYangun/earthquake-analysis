#Importing Libraries
import requests 
import pandas as pd 

def fetch_data(url):
    response = requests.get(url) 

    # Fix encoding to correctly display Turkish characters
    response.encoding = "windows-1254"

    # The actual earthquake data is inside the <pre> tag; everything else 
    # (logo, menu, etc.) is irrelevant, so we extract only this section 
    start = response.text.find("<pre")
    end = response.text.find("</pre>")
    raw_data = response.text[start:end]

    lines = raw_data.split("\n")
    data_lines = lines[7:]
    data_lines = [line for line in data_lines if line.strip() != ""] #delete empty line
    return data_lines



# Takes one earthquake line, splits it into parts, and returns 
#a dictionary with labeled fields (date, time, location, etc.)
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




# Parses every line in the list and collects the results
def all_data_lines(data_lines) :
    #Processing All Data
    earthquakes = []
    for line in data_lines :
        result = parse_line(line)
        earthquakes.append(result)
    return earthquakes




# Converts the list of earthquake dictionaries into a DataFrame 
#and fixes data types so numeric columns can be used for filtering/analysis
def clean_dataframe(earthquakes) :
    df = pd.DataFrame(earthquakes)
    # These columns come in as strings after splitting the text, 
    #so we convert them to float to allow numeric comparisons (e.g. df["ML"] > 4)
    df["latitude"] = df["latitude"].astype(float)
    df["longitude"] = df["longitude"].astype(float)
    df["depth"] = df["depth"].astype(float)
    df["ML"] = df["ML"].astype(float)

    # Kandilli marks unmeasured values with "-.-", which can't be converted 
    #to float directly — we first replace it with NaN, then convert
    df["MD"] = df["MD"].replace("-.-",float("nan"))
    df["Mw"] = df["Mw"].replace("-.-",float("nan"))
    df["MD"] = df["MD"].astype(float)
    df["Mw"] =df["Mw"].astype(float)

# Convert type to day and time
    df["day"] = pd.to_datetime(df["day"], format = "%Y.%m.%d")
    df["time"] = pd.to_datetime(df["time"],format= "%H:%M:%S").dt.time
    df.to_csv("data/earthquakes.csv", index = False)

    return df



url = "http://www.koeri.boun.edu.tr/scripts/lst4.asp"
data_lines = fetch_data(url)
earthquakes = all_data_lines(data_lines)
df = clean_dataframe(earthquakes)