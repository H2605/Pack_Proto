import streamlit as st
import pandas as pd
from keras.layers import Input, Dense, Lambda
from keras.models import Model
from keras import backend as K
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import pickle
import matplotlib.pyplot as plt
import numpy as np
import time


st.title("Einschätzen von Transportschäden")
placeholder = st.empty()
lists=pd.read_csv("lists.csv")
nations=pd.read_csv("all.csv")
lists = lists.loc[:, ~lists.columns.str.contains('^Unnamed')]
lists=lists[['Produktgruppe', 'Menge', 'Gewicht', 'Mass 1', 'Kunden-Nr.', 'Land', 'Zustellercode']]
loaded_model = pickle.load(open('dummy.pkl', 'rb'))

def piechart(data,labels):
    fig, ax1 = plt.subplots(figsize=(5, 5))
    box = ax1.get_position()
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    #ax1.set_position([box.x0, box.y0, box.width * size/10, box.height * size/10])
    a=dataframe["Richtig/Falsch geschätzt"].value_counts().reset_index()
    st.write()
    ax1.pie(data,labels=labels,  autopct='%1.1f%%', shadow=False, startangle=90)
    return st.pyplot(fig)
placeholder = st.empty()
def click_button():
    st.session_state.clicked = True
#    st.session_state.clicked_twice=False
if 'clicked' not in st.session_state:
    st.session_state.clicked = False
if 'clicked_twice' not in st.session_state:
   st.session_state.clicked_twice= False
def click_button_2():
    st.session_state.clicked_twice = True
if 'clicked_change' not in st.session_state:
   st.session_state.clicked_change= False
   placeholder.empty()
def click_button_c():
    st.session_state.clicked_change= True
    st.session_state.clicked_nice = False

if 'clicked_rice' not in st.session_state:
   st.session_state.clicked_rice= False
def click_button_rice():
    st.session_state.clicked_rice = True
if 'clicked_nice' not in st.session_state:
   st.session_state.clicked_nice= False
def click_button_nice():
    st.session_state.clicked_nice = True
    st.session_state.clicked_change = False
#latent_dim = 4
# Laden des gespeicherten Modells
#autoencoder = load_model('/Users/huyduc/Documents/GitHub/Data Augmentation/mein_autoencoder2.h5')
col1, col2 = st.columns(2)


with col1:
    button3=st.button("Eigene Daten eintragen", on_click=click_button_c)
with col2:
    button5=st.button("CSV Datei hochladen", on_click=click_button_nice)

placeholder = st.empty()
with placeholder.container():
    if st.session_state.clicked_change:
        produktgruppe=st.selectbox("Produktgruppe",(lists["Produktgruppe"].unique()))
        menge = st.number_input("Menge", value=0.00,key=1 )
        gewicht = st.number_input("Gewicht", value=0.00,key=2)
        mass1 = st.number_input("Mass 1", value=0.00,key=3)
        kundennr = st.text_input('Kunden Nr.', '',max_chars=5)
        nation=st.selectbox("Land",(nations["name"].unique()))
        zustellercode=st.selectbox("Zustellercode",(lists["Zustellercode"].unique()))
        filter = nations['name'] == nation
        land=nations.loc[filter, 'alpha-2']
        button4=st.button("Transportschaden schätzen", on_click=click_button_rice)
        df2 = pd.DataFrame({
            "Produktgruppe":produktgruppe,
            "Menge":menge,
            "Gewicht":gewicht,
            "Mass 1":mass1,
            "Kunden-Nr.":kundennr,
            "Land":land,
            "Zustellercode":zustellercode})
        if st.session_state.clicked_rice:
            frame_mf=pd.DataFrame(columns=lists.keys())
            frame_mf=frame_mf.append(df2)
            prediction=loaded_model.predict(frame_mf)
            frame_mf["Transportschaden nach ML Modell"]=np.where(prediction>0,1,0)
            st.dataframe(frame_mf)
            if prediction>0.5:
                st.write("Es wird voraussichtlich ein Transportschaden entstehen")
            else:
                st.write("Es wird voraussichtlich kein Transportschaden entstehen")





if st.session_state.clicked_nice:

    st.header("Datenauswahl und Vorschau")
    uploaded_file = st.file_uploader("Datei mit den Lieferungen auswählen")

    try:
        dataframe = pd.read_csv(uploaded_file,index_col=0,dtype={'Kunden-Nr.': object})
        #['Produktgruppe', 'Menge', 'Gewicht', 'Mass 1', 'Kunden-Nr.', 'Land','Zustellercode']
        
        st.subheader("Vorschau der geladenen Daten")
        st.write(dataframe[['Produktgruppe', 'Menge', 'Gewicht', 'Mass 1', 'Kunden-Nr.', 'Land','Zustellercode']].head(5))
        with st.expander("Alle Daten"):
            st.write(dataframe[['Produktgruppe', 'Menge', 'Gewicht', 'Mass 1', 'Kunden-Nr.', 'Land','Zustellercode']])
    #    if st.button('Alle Daten anzeigen lassen', on_click=click_button):
    #        st.write(dataframe[['Produktgruppe', 'Menge', 'Gewicht', 'Mass 1', 'Kunden-Nr.', 'Land','Zustellercode']])
    #    col1, col2 = st.columns(2)
    #    if col1.button('Vorschau anzeigen'):
    #        st.write(dataframe[['Produktgruppe', 'Menge', 'Gewicht', 'Mass 1', 'Kunden-Nr.', 'Land','Zustellercode']].head(10))
    #    if col2.button('Alle Daten anzeigen lassen'):
    #        st.write(dataframe[['Produktgruppe', 'Menge', 'Gewicht', 'Mass 1', 'Kunden-Nr.', 'Land','Zustellercode']])
        X_test=dataframe[['Produktgruppe', 'Menge', 'Gewicht', 'Mass 1', 'Kunden-Nr.', 'Land','Zustellercode']]
        st.button("Transportschaden vorhersagen", on_click=click_button_2)
        if st.session_state.clicked_twice:
                                                                                                            
            predictions = loaded_model.predict(X_test)
            dataframe["Transportschaden nach ML Modell"]=predictions
            dataframe["Transportschaden nach ML Modell"]=np.where(dataframe["Transportschaden nach ML Modell"]>0.5,1,0)
            st.write(dataframe[['Produktgruppe', 'Menge', 'Gewicht', 'Mass 1', 'Kunden-Nr.', 'Land','Zustellercode','Transportschaden nach ML Modell']])
            dataframe["Schaden"]=np.where(dataframe["Transportschaden nach ML Modell"]==1,"Schaden","Kein Schaden")
            #st.bar_chart(dataframe["Transportschaden nach ML Modell"].value_counts())
            transp_df=dataframe['Schaden'].value_counts().reset_index()
            series_b=dataframe["Schaden"].value_counts(normalize=True).mul(100).round(1).astype(str) + '%'
            series_b=series_b.to_list()
            df_b=dataframe["Schaden"].value_counts().reset_index()
            
            df_b["Schaden in %"]=series_b

            st.write(df_b)
            fig = plt.figure(figsize =(10, 7))
            #st.write(dataframe['Klassifizierung'].value_counts().plot(kind='bar'))
            plt.bar(dataframe['Schaden'].unique(),transp_df["Schaden"] )
            # Show Plot
            st.pyplot(fig)


        
            state1=st.session_state
            st.header("Evaluation")
            eval_file = st.file_uploader("Ergebnisse zu den Lieferungen dazu auswählen")
            eval_df=pd.read_csv(eval_file)
            dataframe["Transportschaden"]=eval_df["Transportschaden"]
            button1=st.button("Evaluation", on_click=click_button)
            if state1.clicked:
                st.header("Geschätzter Transportschaden vs realer Transportschaden")

                dataframe["Richtig/Falsch geschätzt"]=np.where(dataframe["Transportschaden nach ML Modell"]-dataframe["Transportschaden"]==0,"Richtig","Falsch")
                st.write(dataframe[['Produktgruppe', 'Menge', 'Gewicht', 'Mass 1', 'Kunden-Nr.', 'Land','Zustellercode','Transportschaden',"Transportschaden nach ML Modell","Richtig/Falsch geschätzt"]])
                list_klassi=[]
                
                for i in range(len(dataframe)):
                    if dataframe["Transportschaden nach ML Modell"][i]-dataframe["Transportschaden"][i]==0:
                        list_klassi.append("Richtig eingeschätzt")
                    if dataframe["Transportschaden nach ML Modell"][i]-dataframe["Transportschaden"][i]==1:
                        list_klassi.append("Transportschaden erwartet, aber nicht enstanden")
                    if dataframe["Transportschaden nach ML Modell"][i]-dataframe["Transportschaden"][i]==-1:
                        list_klassi.append("Transportschaden nicht erwartet, aber enstanden")


                frame=dataframe["Richtig/Falsch geschätzt"].value_counts().reset_index()
                richtig=frame["Richtig/Falsch geschätzt"][0]
                res=round((richtig/len(dataframe))*100,2)
                res=str(res)
                st.write("Das Modell hat die Tranportschäden mit einer Genauigkeit von ",res,"% richtig vorhergesagt")
                
                #st.write(dataframe["Richtig/Falsch geschätzt"].value_counts())

                #st.subheader("Kreisdiagramm")
                labels = 'Richtig', 'Falsch',"Transportschaden erwartet aber nicht eingetreten","Transportschaden nicht erwartet, aber enstanden"
                #size = st.slider('Auflösung des Kreisdiagramms einstellen', 1, 20, 10)
                dataframe["Klassifizierung"]=list_klassi
                #piechart(dataframe["Klassifizierung"].value_counts(),labels=dataframe["Klassifizierung"].unique())
                #st.subheader("Balkendiagramm")
                klassi_df_a=dataframe["Klassifizierung"].value_counts(normalize=True).mul(100).round(1).astype(str) + '%'
                #klassi_df_a["Klassifizierung in %"]=klassi_df_a["Klassifizierung"]
                df_a=klassi_df_a.to_list()
                klassi_df=dataframe['Klassifizierung'].value_counts().reset_index()
                klassi_df["Klassifizierung in %"]=df_a#["Klassifizierung in %"]
                st.write(klassi_df)
                fig = plt.figure(figsize =(10, 7))

                plt.xticks(rotation=65)
                #st.write(dataframe['Klassifizierung'].value_counts().plot(kind='bar'))
                plt.bar(dataframe['Klassifizierung'].unique(),klassi_df["Klassifizierung"] )
                # Show Plot
                st.pyplot(fig)

                #plt.xlabel('Klassifizierung')
                #plt.ylabel('Anzahl')

                # Titel hinzufügen
                plt.title('Beispiel Balkendiagramm')

            
    except ValueError:
        st.error('Datei bitte hochladen')