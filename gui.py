import streamlit as st
import pyperclip
from csv_to_excel_2 import csv_to_excel

st.title("Alles für den Kassier")

# "Um den Pfad der .csv Datei zu kopieren, einfach im Explorer mit Rechtsklick auf die Datei gehen und <Pfad kopieren> auswählen"

# st.text_input("Pfad zur .csv Datei hier einfügen", key="path_to_csv")

# if st.session_state.path_to_csv:
#   df = csv_to_excel(st.session_state.path_to_csv)
#   st.write(df)

#   copy = st.button("Kopiere Tabelleninhalt")
#   if copy:
#     df.to_clipboard(index=False, header=False)

uploaded_file = st.file_uploader("Wähle die aus Elba exportierte .csv Datei aus")
if uploaded_file:
  df = csv_to_excel(uploaded_file)
  st.write(df)

  copy = st.button("Kopiere Tabelleninhalt")
  if copy:
    pyperclip.copy(df.to_string(header=False, index= False))
    #df.to_clipboard(index=False, header=False)
    st.success("Text wurde kopiert")