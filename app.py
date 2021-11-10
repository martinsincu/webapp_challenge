import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import datasets
import json
import boto3


import requests

url = 'https://hrgh3f7u5a.execute-api.us-east-2.amazonaws.com/fraudemodel/'
data1 = '{  "data": {"columns":["hora","dia","establecimiento_No_definido","ciudad_No_definido","interes_tc_cat_A_<40]","linea_tc_cat_A_<44000]","device_score_1"],"index":[9],"data":[[18,5,0,1,1,0,0]]}   }'

response1 = requests.post(url, data=data1, headers={"Content-Type": "application/json"})


if st.button('Predict'):
	st.write('Predictions1:', response1.json())
else:
	st.write('Goodbye')

st.title("Hello AWS!")




def main():
	activities=['EDA','model','summary']
	option=st.sidebar.selectbox('Selection option:',activities)

	
#DEALING WITH THE EDA PART

	if option=='EDA':
		st.subheader("Exploratory Data Analysis")


#DEALING WITH THE VISUALISATION PART

	elif option=='Visualisation':
		st.subheader("Data Visualisation")

	# DEALING WITH THE MODEL BUILDING PART

	elif option=='model':
		st.subheader("Model")

	
#DELING WITH THE ABOUT US PAGE
	elif option=='summary':

		st.markdown('This is an interactive web page for our ML project, <add more> .')


if __name__ == '__main__':
	main() 