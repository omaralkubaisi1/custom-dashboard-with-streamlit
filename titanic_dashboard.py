import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = r"/Users/omarkubaisi/Desktop/custom dashboard with streamlit/Titanic Data.csv"

try:
    titanic_data = pd.read_csv(file_path, sep=None, engine="python", on_bad_lines="skip")
except Exception as e:
    st.error(f"Virhe tiedoston lukemisessa: {e}")
    st.stop()

for col in ['Age', 'Pclass', 'Survived']:
    if col in titanic_data.columns:
        titanic_data[col] = pd.to_numeric(titanic_data[col], errors='coerce')

if 'Ticket' in titanic_data.columns:
    titanic_data['Ticket'] = titanic_data['Ticket'].astype(str)

st.title("Titanic Data Analysis")
st.write("Titanic-data:")
st.dataframe(titanic_data)

if 'Age' in titanic_data.columns and titanic_data['Age'].notna().any():
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(titanic_data['Age'].dropna(), kde=True, bins=20, color='skyblue', ax=ax)
    ax.set_title('Titanicin matkustajien ikäjakauma', fontsize=16)
    ax.set_xlabel('Ikä (vuosina)', fontsize=14)
    ax.set_ylabel('Matkustajien lukumäärä', fontsize=14)
    ax.grid(True, linestyle='--', alpha=0.7)
    st.pyplot(fig)

for feature, title, palette in [('Sex', 'Sukupuolen jakauma', "pastel"), 
                                 ('Pclass', 'Matkustajaluokan jakauma', "muted"), 
                                 ('Survived', 'Selviytyminen Titanicissa', "coolwarm")]:
    if feature in titanic_data.columns:
        count_data = titanic_data[feature].value_counts()
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(x=count_data.index, y=count_data.values, palette=palette, ax=ax)
        ax.set_title(title, fontsize=16)
        ax.set_xlabel(feature, fontsize=12)
        ax.set_ylabel('Määrä', fontsize=12)
        st.pyplot(fig)

if 'Age' in titanic_data.columns and titanic_data['Age'].notna().any():
    selected_age = st.slider('Valitse ikä', int(titanic_data['Age'].min()), int(titanic_data['Age'].max()), int(titanic_data['Age'].min()))
    st.write(f'Valitsit iän: {selected_age}')

for feature in ['Sex', 'Pclass', 'Survived']:
    if feature in titanic_data.columns:
        selected_value = st.selectbox(f"Valitse {feature}", sorted(titanic_data[feature].dropna().unique()))
        filtered_data = titanic_data[titanic_data[feature] == selected_value]
        st.write(f"Data {feature}: {selected_value}")
        st.dataframe(filtered_data)
