import streamlit as st
import pydeck as pdk
import pandas as pd
import random as rd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
pd.set_option("display.max_rows", None, "display.max_columns", None, 'display.width', None, 'max_colwidth', None)
st.set_option('deprecation.showPyplotGlobalUse', False)

'''
Name:       Ryan Neiser
CS230:      Section 5
Data:       RollerCoasters Geo
URL:        Link to your web application on Streamlit Cloud (if posted) 

Description:    

This program includes... 
Python Features:
•	A function with two or more parameters, one of which has a default value: topSpeedWidget()
•	A function that returns more than one value: dictionaryOfParks() 
•	A function that you call at least two different places in your program: readDataPandas() in main() and pivotTable()
•	A list comprehension: readDataList()
•	A loop that iterates through items in a list, dictionary, or data frame: dictionaryOfParks()
•	At least two different methods of lists, dictionaries, or tuples.

Streamlit Features:

•	At least three Streamlit different widgets: topSpeedWidget(), selectBox(), and textInput()
•	Page design features: images as custom icons in map, pivot table in side bar

Visualizations:

•	At least three different charts with titles, colors, labels, legends, as appropriate: linePlot(ogDF), pieChart1(ogDF), pieChart2(ogDF)
•	At least one detailed map: generateMap()

Data Analytics Capabilities:

•	Sorting data in ascending or descending order, by one or more columns: linePlot()
•	Filtering data by one condition: generateMap() line 3
•	Filtering data by two or more conditions with AND or OR: linePlot()
•	Analyzing data with pivot tables: pivotTable()

'''
path = "C:/Users/17747/OneDrive - Bentley University/CS230/finalProject/"
def readDataList(path):
    r_file = open(path + "RollerCoasters-Geo.csv", "r")
    line_list = r_file.readlines()
    r_file.close()

    cleanList = []
    count = 0
    for z in line_list:
        if count>0:
            a = z.split(",")
            cleanList.append(a)
        count=+1

    return cleanList


def readDataPandas(path):
    df_all_data = pd.read_csv(path + "RollerCoasters-Geo.csv")
    return df_all_data

def dictionaryOfParks(list):
    dict = {}
    x = 0
    for i in list:
        if x != 0:
            if i[2] not in dict:
                dict[i[2]] = [i[1]]
            else:
                dict[i[2]].append(i[1])
        x += 1

    park_list = []
    for i in dict.keys():
        park_list.append(i)
    return dict, park_list

def dictionaryOfInversions(list):
    dict = {}
    x = 0
    for i in list:
        if x != 0:
            key = i[16].strip('\n')
            if key not in dict:
                dict[key] = [i[1]]
            else:
                dict[key].append(i[1])
        x += 1

    inversions_list = []
    for i in dict.keys():
        inversions_list.append(i)
    return dict, inversions_list

def lowAndHighSpeeds(data):
    low = 9999999
    high = -9999999
    for i in data:
        if i[10] != '':
            if int(i[10]) > high:
                high = int(i[10])

            if int(i[10]) < low:
                low = int(i[10])

    return low, high

def topSpeedWidget(data, low = 0, high = 200):
    select_num = st.slider("Select the Top Speed you Desire", low, high)
    ride_list = []
    for i in data:
        if i[10] != '':
            if int(i[10]) == select_num:
                ride_list.append(i[1])
    st.write(f"The rides that match this top speed are: {ride_list}")

def selectBox(dict, list):
    selected_box = st.selectbox("Select a Park to See its Rides", list)
    st.write(dict[selected_box])

def textInput(dict):
    inv_num = st.text_input("Enter Your Desired Amount of Inversions", 0, 10)
    st.write(f"The Rides with {inv_num} inversion(s) are: {dict[inv_num]}")

def generateMap():
    st.title("Map of Theme Parks")
    df_rol = pd.read_csv(path + "RollerCoasters-Geo.csv")
    sub_rol = df_rol[df_rol.Park.str.lower() != ''][['Park', 'Latitude', 'Longitude']]
    # Map data must contain a column named "latitude" or "lat"

    sub_rol.rename(columns={"Latitude": "lat", "Longitude": "lon"}, inplace=True)  # lat and lon must be lowercase

    # Create custom icons
    ICON_URL = "https://upload.wikimedia.org/wikipedia/commons/6/6b/Map_marker_icon_%E2%80%93_Nicolas_Mollet_%E2%80%93_Ferris_wheel_%E2%80%93_Culture_%26_Entertainment_%E2%80%93_White.png"  # Get the custom icon online
    # Icon or picture finder: https://commons.wikimedia.org/

    # Format your icon
    icon_data = {
        "url": ICON_URL,
        "width": 100,
        "height": 100,
        "anchorY": 100
    }

    # Add icons to your dataframe
    sub_rol["icon_data"] = None
    for i in sub_rol.index:
        # df_bos["icon_data"][i] = icon_data does the same thing as below
        sub_rol.at[i, "icon_data"] = icon_data

    # Create a layer with your custom icon
    icon_layer = pdk.Layer(type="IconLayer",
                           data=sub_rol,
                           get_icon="icon_data",
                           get_position='[lon,lat]',
                           get_size=4,
                           size_scale=10,
                           pickable=True)

    # Create a view of the map: https://pydeck.gl/view.html
    view_state = pdk.ViewState(
        latitude=37.0902,
        # sub_rol["lat"].mean(),
        longitude=-95.7129,
        # sub_rol["lon"].mean(),
        zoom=3,
        pitch=0
    )

    # stylish tool tip: https://pydeck.gl/tooltip.html?highlight=tooltip
    tool_tip = {"html": "Park Name:<br/> <b>{Park}</b>",
                "style": {"backgroundColor": "orange",
                          "color": "white"}
                }

    icon_map = pdk.Deck(
        map_style='mapbox://styles/mapbox/navigation-day-v1',
        layers=[icon_layer],
        initial_view_state=view_state,
        tooltip=tool_tip)

    st.pydeck_chart(icon_map)

def linePlot(df_rol):
    sub_rol = df_rol[(df_rol.Type.str.lower() == 'wooden')&(df_rol.Age_Group.str.lower() == '1:older')][['Length','Year_Opened']]
    sub_rol.dropna(inplace=True)
    sub_rol.sort_values("Year_Opened", inplace=True)
    sub_rol.set_index("Year_Opened", inplace=True)

    sub_rol.plot()

    plt.xlabel("Years")
    plt.ylabel("Length")
    plt.title("Length of Older, Wooden Roller Coasters Over Years")
    plt.legend().remove()

    st.pyplot()

def pieChart1(df_rol):
    fig, ax = plt.subplots()
    ax.pie(df_rol['Type'].value_counts(), labels=df_rol['Type'].unique(), autopct='%1.1f%%')
    ax.set_title('Roller Coaster Material Distribution')

    st.pyplot(fig)

def pieChart2(df_rol):
    fig, ax = plt.subplots()
    ax.pie(df_rol['State'].value_counts(), labels=df_rol['State'].unique(), autopct='%1.1f%%')
    ax.set_title('Roller Coaster State Distribution')

    st.pyplot(fig)
    pass

def pivotTable():
    df = readDataPandas("C:/Users/17747/OneDrive - Bentley University/CS230/finalProject/")

    df.dropna(inplace=True)
    df6 = pd.pivot_table(data=df, index=["Age_Group"], columns=["Type"], values=["Max_Height", "Drop"], aggfunc=np.average)
    st.sidebar.write(df6)

def main():
    dataList = readDataList(path)
    ogDF = readDataPandas(path)
    rollerDict, park_list = dictionaryOfParks(dataList)
    inversionsDict, inversions_list = dictionaryOfInversions(dataList)
    low_speed, high_speed = lowAndHighSpeeds(dataList)
    st.write(f"low speed is {low_speed} and high speed is {high_speed}")
    topSpeedWidget(dataList, low_speed, high_speed)
    selectBox(rollerDict, park_list)
    textInput(inversionsDict)
    linePlot(ogDF)
    pieChart1(ogDF)
    pieChart2(ogDF)
    pivotTable()
    generateMap()

main()