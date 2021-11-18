import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import datasets
import json
import boto3

import requests
from scipy.stats import chi2_contingency
import seaborn as sns

from io import BytesIO
from PIL import Image
response = requests.get("https://raw.githubusercontent.com/martinsincu/deploy_mlflow_aws/master/images/technologies.PNG")
img = Image.open(BytesIO(response.content))

st.title("DS Challenge!")



def main():
	activities=['Model','EDA'] # summary
	option=st.sidebar.selectbox('Selection option:',activities)

	
#DEALING WITH THE EDA PART

	if option=='Model':
		st.subheader("Model")

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
		output = int(response1.json())

		if output>=1:
			label = 'Fraude'
		else:
			label = 'NoFraude'

		if st.button('Predict'):
			st.write('Predictions:', response1.json(), " -> ", label)
		


#DEALING WITH THE VISUALISATION PART

	elif option=='Visualisation':
		st.subheader("Data Visualisation")

	# DEALING WITH THE MODEL BUILDING PART

	elif option=='EDA':
		st.subheader("Exploratory Data Analysis")

		data=st.file_uploader("Upload dataset:",type=['csv','xlsx','txt','json'])
		
		if data is not None:
			st.success("Data successfully loaded")

			Data_raw = pd.read_csv(data)
			st.dataframe(Data_raw.head(3))

			if st.checkbox("Display shape"):
				st.write(Data_raw.shape)
			if st.checkbox('Display Null Values'):
				st.write(Data_raw.isnull().sum())
			if st.checkbox("Display the data types"):
				st.write(Data_raw.dtypes.to_dict())

			Data_raw['fraude'] = Data_raw['fraude'].astype(int)
			Data_raw['is_prime'] = Data_raw['is_prime'].astype(int)

			if st.checkbox("Display column dispositivo"):
				st.write(Data_raw['dispositivo'].value_counts(dropna=False))

			dispositivo_json_cols = list(eval(Data_raw['dispositivo'].loc[0]).keys())

			list_data = list(Data_raw['dispositivo'].apply( lambda x: list( map(lambda x:str(x),list(eval(x).values()))) ) )
			Data_raw.loc[:,dispositivo_json_cols] = pd.DataFrame(list_data,columns = dispositivo_json_cols)

			Data_raw.drop(['dispositivo'], axis=1, inplace=True)
			Data_raw.drop(['model'], axis=1, inplace=True)
			
			if st.checkbox("Display fraude ratio (transactions)"):
				st.write(Data_raw['fraude'].value_counts(normalize=True))

			vars_obs = ['fraude', 'tipo_tc', 'is_prime', 'genero', 'status_txn', 'os', 'ciudad', 'device_score', 'establecimiento']
			if st.checkbox("Display values of object columns"):
				st.write([col+' : '+str(list(Data_raw[col].factorize(na_sentinel=None)[1])) for col in vars_obs])

			Data_raw['establecimiento'] = Data_raw['establecimiento'].fillna('No_definido')
			Data_raw['ciudad'] = Data_raw['ciudad'].fillna('No_definido')
			Data_raw['genero'] = Data_raw['genero'].replace({ "--" : "No_definido"})
			Data_raw['os'] = Data_raw['os'].replace({ "%%" : "PERCENT" , "." : "POINT" })
			Data_raw['tipo_tc'] = Data_raw['tipo_tc'].replace({ "Física" : "Fisica" })

			# Data a Nivel Cliente
			Data_df = Data_raw.groupby('ID_USER').\
			apply(lambda x: pd.Series(dict(
			   
			    cant_trxs = x['ID_USER'].count(),

			    ciudad_mode = x['ciudad'].mode()[0], 
			    os_mode = x['os'].mode()[0],   
			    device_score_mode = x['device_score'].mode()[0],
			    establecimiento_mode = x['establecimiento'].mode()[0], 
			    tipo_tc_mode = x['tipo_tc'].mode()[0],
			    
			    monto_mean = x['monto'].mean(),
			    monto_median = x['monto'].median(),
			    monto_total = x['monto'].sum(),
			    
			    fraude = x['fraude'].max()
			)))

			if st.checkbox("Display customers dataframe"):
				st.dataframe(Data_df.head(3))
			if st.checkbox("Display fraude ratio (customers)"):
				st.write(Data_df['fraude'].value_counts(normalize=True))
			if st.checkbox("Display shape(customers)"):
				st.write(Data_df.shape)

			vars_num = ['fraude', 'cant_trxs', 'monto_mean', 'monto_median', 'monto_total']
			vars_object = ['tipo_tc_mode', 'os_mode', 'ciudad_mode', 'device_score_mode', 'establecimiento_mode']
			df = Data_df[vars_object+['fraude']]


			factors_paired = [(i,j) for i in df.columns.values for j in df.columns.values] 
			chi2, p_values =[], []

			for f in factors_paired:
			    if f[0] != f[1]:
			        chitest = chi2_contingency(pd.crosstab(df[f[0]], df[f[1]]))   
			        chi2.append(chitest[0])
			        p_values.append(chitest[1])
			    else:      # for same factor pair
			        chi2.append(0)
			        p_values.append(0)

			chi2 = np.array(chi2).reshape((6,6)) # shape it as a matrix
			chi2 = pd.DataFrame(chi2, index=df.columns.values, columns=df.columns.values) # then a df for convenience
			
			if st.checkbox("Display Correlation of categorical variables"):
				st.write(chi2)


			target = 'fraude'
			aux_list = []
			for col in ['establecimiento_mode','tipo_tc_mode','os_mode','ciudad_mode']:
			    print(col)
			    aux = pd.concat([Data_df[col].value_counts(dropna=False).rename("#").sort_index(),
			                    Data_df.groupby([col], dropna=False)[target].sum().rename("Target").sort_index(),
			                    Data_df[col].value_counts(dropna=False, normalize=True).rename("per").sort_index()],axis=1)
			    aux["Per_A"]=aux['per'].cumsum(axis=0)
			    aux["efec_T"]=aux['Target']/aux['#']
			    aux["per_Target"]=aux['Target']/(aux['Target'].sum())
			    aux["Per_Tg_A"]=aux['per_Target'].cumsum(axis=0)
			    #print(aux)
			    aux.index = col+'_'+aux.index 
			    aux_list.append(aux)
			    #print("-------------------------------------------------")
			aux_list = pd.concat(aux_list)

			if st.checkbox("Display categorical variables details"):
				st.write(aux_list)
			
			corr_df = Data_df.corr()
			st.set_option('deprecation.showPyplotGlobalUse', False)

			if st.checkbox("Display Heatmap"):
				st.write(sns.heatmap(corr_df, cmap="coolwarm", linewidths=.5, square=True, annot=True, fmt='.3f'))
				st.pyplot()
			
			Data_F = Data_df[['cant_trxs','monto_total','establecimiento_mode','tipo_tc_mode','fraude']]

			if st.checkbox("Display Boxplot"):
				for cat in ['establecimiento_mode','tipo_tc_mode']:
				    for num in ['cant_trxs','monto_total']: 
				        #plt.subplots(figsize=(15, 5))
				        st.write(sns.boxplot(x=cat, y=num, data=Data_F, palette='rainbow', hue="fraude" ))
				        st.pyplot()

			if st.checkbox("Display Countplot"):
				for col in ['establecimiento_mode','tipo_tc_mode']:
				    plt.subplots(figsize=(15, 5))
				    st.write(sns.countplot(x=col,data=Data_F, hue="fraude"))
				    st.pyplot()

			if st.checkbox("Display Histplot"):
				for col in ['cant_trxs','monto_total']:
					plt.subplots(figsize=(15, 5))
					st.write(sns.histplot(data=Data_F, x=col, hue="fraude", element="step", stat="density", common_norm=False))
					st.pyplot()

			Data_F['cant_trxs_Q'] = pd.qcut(Data_F['cant_trxs'], 4, labels=['q1','q2','q3','q4'])
			Data_F['monto_total_Q'] = pd.qcut(Data_F['monto_total'], 4, labels=['q1','q2','q3','q4'])

			aux = Data_F.groupby(['tipo_tc_mode','establecimiento_mode','cant_trxs_Q']).agg( # monto_total_Q
			    cant = ('fraude', 'count'),
			    fraude_avg = ('fraude', 'mean'),
			    fraude_sum = ('fraude', 'sum')
			).reset_index()

			aux = aux[aux['cant']>0]
			aux['cant_per'] =  aux['cant']/aux['cant'].sum()
			aux['fraude_per'] =  aux['fraude_sum']/aux['fraude_sum'].sum()
			aux['new'] =  aux['cant_per']*aux['fraude_avg']
			aux = aux.sort_values(by=['new','cant_per'], ascending=[False,False])
			aux["fraude_per_A"]=aux['fraude_per'].cumsum(axis=0)

			if st.checkbox("Display Agrupation Detail"):
				st.write(aux)

			Data_F['segment_fraude'] = 'Bajo'
			Data_F['segment_fraude'] = Data_F[['tipo_tc_mode','establecimiento_mode','cant_trxs_Q','segment_fraude']]\
			    .apply(lambda x: 'Alto' if (x[0]=='Fisica' and x[1]=='No_definido' and x[2] in ['q2','q3','q4'] ) else x[3], axis=1)
			Data_F['segment_fraude'] = Data_F[['tipo_tc_mode','establecimiento_mode','cant_trxs_Q','segment_fraude']]\
			    .apply(lambda x: 'Medio' if (x[0]=='Fisica' and x[1]!='No_definido' and x[2] in ['q2','q3','q4'] ) else x[3], axis=1)
			
			df_plot = Data_F.groupby('segment_fraude',as_index=False).agg(
			    customers = ('fraude', 'count'),
			    customers_fraude = ('fraude', 'sum'),
			    fraude_ratio = ('fraude', 'mean'),
			)
			df_plot['share_fraude'] = df_plot['customers_fraude'] / df_plot['customers_fraude'].sum()

			if st.checkbox("Display Segments"):
				st.write(df_plot)
				st.write(sns.barplot(data = df_plot, x='segment_fraude',y='share_fraude',order=['Bajo','Medio','Alto']))
				plt.title('Distribution of fraudster per Segment')
				st.pyplot()

	
#DELING WITH THE ABOUT US PAGE
	elif option=='summary':

		st.markdown('This is an interactive web page for our ML project, <add more> .')


if __name__ == '__main__':
	main() 