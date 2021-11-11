import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import datasets
import json
import boto3

import requests


from io import BytesIO
from PIL import Image
response = requests.get("https://raw.githubusercontent.com/martinsincu/deploy_mlflow_aws/master/images/technologies.PNG")
img = Image.open(BytesIO(response.content))

st.title("DS Challenge!")

st.subheader('Fraude Solution')

st.write("This is simple Web APP to use REST API from AWS Gateway.")
st.write("The figure below shows the intereacttion of the API. check the repo: "+'https://github.com/martinsincu/deploy_mlflow_aws')


st.image(img,use_column_width=True)

#### Inputs for the Model

# Select button - DIA
dia_name = st.selectbox("Indicate a Day",('Monday','Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'))
semana = {'Monday':0,'Tuesday':1, 'Wednesday':2, 'Thursday':3, 'Friday':4, 'Saturday':5, 'Sunday':6}
st.write("Your day is : ", dia_name)
dia = semana[dia_name]
st.write("coded as : ", dia)

# slider - HORA
hora = st.slider('Indicate an Hour', 0, 23, 12)
st.write("Your hour is : ", hora)

# Select button - ESTABLECIMIENTO
establishment_name  = st.selectbox("Choose an establishment", ('Restaurante','Abarrotes','Super','MPago','Farmacia','No_definido') )
st.write("Your establishment is : ", establishment_name)
if establishment_name=='No_definido':
	establecimiento_No_definido = 1
else:
	establecimiento_No_definido = 0
st.write("coded as : : ", establecimiento_No_definido)


# Select button - CIUDAD
city_name =st.selectbox("Choose a City", ('Toluca','Guadalajara','Merida','Monterrey','No_definido') )
st.write("Your City is : ", city_name)
if city_name=='No_definido':
	ciudad_No_definido = 1
else:
	ciudad_No_definido = 0
st.write("coded as : : ", ciudad_No_definido)


# slider - DEVICE SCORE
device_score = st.slider('Indicate Device Score', 1, 5, 3)
st.write("Your Device Score is : ", device_score)
if device_score==1:
	device_score_1 = 1
else:
	device_score_1 = 0
st.write("coded as : : ", device_score_1)


# slider - INTERES TC
interes_num = st.slider('Indicate Credit Card Interest', 32, 64, 40)
st.write("Your Credit Card Interest is : ", interes_num)
if interes_num<40:
	interes_40 = 1
else:
	interes_40 = 0
st.write("coded as : : ", interes_40)

# slider - LINEA TC
linea_num = st.slider('Indicate Credit Card Line', 25000, 99000, 30000)
st.write("Your Credit Card Line is : ", linea_num)
if linea_num<44000:
	linea_tc_44000 = 1
else:
	linea_tc_44000 = 0
st.write("coded as : : ", linea_tc_44000)


url = 'https://hrgh3f7u5a.execute-api.us-east-2.amazonaws.com/fraudemodel/'
data = '{  "data": {"columns":["hora","dia","establecimiento_No_definido","ciudad_No_definido","interes_tc_cat_A_<40]","linea_tc_cat_A_<44000]","device_score_1"],"index":[9],"data":[[%s,%s,%s,%s,%s,%s,%s]]} }' % (hora, dia, establecimiento_No_definido, ciudad_No_definido, interes_40, linea_tc_44000, device_score_1)

st.markdown("**API url:**&nbsp;&nbsp;&nbsp"+"`https://hrgh3f7u5a.execute-api.us-east-2.amazonaws.com/fraudemodel/`")

response1 = requests.post(url, data=data, headers={"Content-Type": "application/json"})

if response1==1:
	label = 'Fraude'
else:
	label = 'NoFraude'

if st.button('Predict'):
	st.write('Predictions:', response1.json(), " -> ",label)




def main():
	activities=['Model','EDA','summary']
	option=st.sidebar.selectbox('Selection option:',activities)

	
#DEALING WITH THE EDA PART

	if option=='Model':
		st.subheader("Model")
		


#DEALING WITH THE VISUALISATION PART

	elif option=='Visualisation':
		st.subheader("Data Visualisation")

	# DEALING WITH THE MODEL BUILDING PART

	elif option=='EDA':
		st.subheader("Exploratory Data Analysis")

	
#DELING WITH THE ABOUT US PAGE
	elif option=='summary':

		st.markdown('This is an interactive web page for our ML project, <add more> .')


if __name__ == '__main__':
	main() 