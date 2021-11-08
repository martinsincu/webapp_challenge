import streamlit as st

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