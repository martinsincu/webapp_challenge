import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import datasets
import json
import boto3


import requests

url = 'https://u5r8ezc3el.execute-api.us-east-2.amazonaws.com/mlmodel'

data1 = '{  "data": {"columns":[0,1],"index":[11],"data":[[4.6,1.5]]}   }'
data2 = '{  "data": {"columns":[0,1],"index":[11],"data":[[1.6,0.6]]}   }'
response1 = requests.post(url, data=data1, headers={"Content-Type": "application/json"})
response2 = requests.post(url, data=data2, headers={"Content-Type": "application/json"})


if st.button('Predict'):
	st.write('Predictions1:', response1.json())
	st.write('Predictions2:', response2.json())
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