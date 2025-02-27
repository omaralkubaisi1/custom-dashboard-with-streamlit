import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Lue Titanic data CSV-tiedostosta
file_path = r"/Users/omarkubaisi/Desktop/custom dashboard with streamlit/Titanic Data.csv"

# Yritetään lukea CSV-tiedosto ja määritetään erotin automaattisesti
try:
    titanic_data = pd.read_csv(file_path, sep=None, engine="python", on_bad_lines="skip")
except Exception as e:
    st.error(f"Virhe tiedoston lukemisessa: {e}")
    st.stop()

# Muunnetaan sarakkeet oikeaan muotoon
if 'Age' in titanic_data.columns:
    titanic_data['Age'] = pd.to_numeric(titanic_data['Age'], errors='coerce')

if 'Pclass' in titanic_data.columns:
    titanic_data['Pclass'] = pd.to_numeric(titanic_data['Pclass'], errors='coerce')

if 'Survived' in titanic_data.columns:
    titanic_data['Survived'] = pd.to_numeric(titanic_data['Survived'], errors='coerce')

if 'Ticket' in titanic_data.columns:
    titanic_data['Ticket'] = titanic_data['Ticket'].astype(str)

# Näytä pääotsikko
st.title("Titanic Data Analysis")

# Näytä data taulukkomuodossa
st.write("Titanic-data:")
st.dataframe(titanic_data)

# Ikäjakauman visualisointi
if 'Age' in titanic_data.columns and titanic_data['Age'].notna().any():
    st.write("Titanicin matkustajien ikäjakauma:")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(titanic_data['Age'].dropna(), kde=True, bins=20, color='skyblue', ax=ax)
    
    ax.set_title('Titanicin matkustajien ikäjakauma', fontsize=16)
    ax.set_xlabel('Ikä (vuosina)', fontsize=14)
    ax.set_ylabel('Matkustajien lukumäärä', fontsize=14)  # Korjattu termi
    ax.grid(True, linestyle='--', alpha=0.7)  # Parannettu luettavuutta
    
    st.pyplot(fig)


# Sukupuolen jakauma
if 'Sex' in titanic_data.columns:
    st.write("Titanicin sukupuolen jakauma:")
    gender_count = titanic_data['Sex'].value_counts()
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x=gender_count.index, y=gender_count.values, palette="pastel", ax=ax)
    ax.set_title('Sukupuolen jakauma', fontsize=16)
    ax.set_xlabel('Sukupuoli', fontsize=12)
    ax.set_ylabel('Määrä', fontsize=12)
    st.pyplot(fig)

# Matkustajaluokan jakauma
if 'Pclass' in titanic_data.columns:
    st.write("Titanicin matkustajaluokan jakauma:")
    class_count = titanic_data['Pclass'].value_counts()
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x=class_count.index, y=class_count.values, palette="muted", ax=ax)
    ax.set_title('Matkustajaluokan jakauma', fontsize=16)
    ax.set_xlabel('Matkustajaluokka', fontsize=12)
    ax.set_ylabel('Määrä', fontsize=12)
    st.pyplot(fig)

# Selviytyneiden jakauma
if 'Survived' in titanic_data.columns:
    st.write("Titanicin selviytyneiden jakauma:")
    survival_count = titanic_data['Survived'].value_counts()
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x=survival_count.index, y=survival_count.values, palette="coolwarm", ax=ax)
    ax.set_title('Selviytyminen Titanicissa', fontsize=16)
    ax.set_xlabel('Selviytyminen (0=Ei, 1=Kyllä)', fontsize=12)
    ax.set_ylabel('Määrä', fontsize=12)
    st.pyplot(fig)

# Interaktiivinen ikävalitsin
if 'Age' in titanic_data.columns and titanic_data['Age'].notna().any():
    min_age = int(titanic_data['Age'].min(skipna=True))
    max_age = int(titanic_data['Age'].max(skipna=True))
    selected_age = st.slider('Valitse ikä', min_value=min_age, max_value=max_age, value=min_age)
    st.write(f'Valitsit iän: {selected_age}')

# Interaktiivinen sukupuolivalitsin
if 'Sex' in titanic_data.columns:
    selected_gender = st.selectbox("Valitse sukupuoli", titanic_data['Sex'].unique())
    filtered_data = titanic_data[titanic_data['Sex'] == selected_gender]
    st.write(f"Data {selected_gender} matkustajista")
    st.dataframe(filtered_data)

# Interaktiivinen matkustajaluokka valitsin
if 'Pclass' in titanic_data.columns:
    selected_class = st.selectbox("Valitse matkustajaluokka", sorted(titanic_data['Pclass'].dropna().unique()))
    class_data = titanic_data[titanic_data['Pclass'] == selected_class]
    st.write(f"Data matkustajaluokassa {selected_class}")
    st.dataframe(class_data)

# Interaktiivinen selviytymisen valitsin
if 'Survived' in titanic_data.columns:
    selected_survival = st.selectbox("Valitse selviytymisstatus", sorted(titanic_data['Survived'].dropna().unique()))
    survival_data = titanic_data[titanic_data['Survived'] == selected_survival]
    st.write(f"Data selviytyneistä: {selected_survival}")
    st.dataframe(survival_data)