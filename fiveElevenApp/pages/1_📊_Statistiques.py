import streamlit as st

cols = st.columns(3)

with cols[0]:
    st.metric(":trophy: Meilleur.re Buteur.se : ", "Rémi Jaylet")
    st.metric(":soccer: Nombre de buts inscrits : ", 11)