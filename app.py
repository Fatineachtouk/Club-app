import streamlit as st
import pandas as pd
import random
from io import BytesIO

# Header
st.image("logo_sans_bg.png", width=150)
st.title("App de gestion des formations du Club Speak Up")

st.write("Bienvenue, chers membres du club Speak Up, dans cet espace où vous pouvez vous inscrire avant d’assister à chaque formation. Le processus prend seulement quelques secondes, mais il aidera énormément le club !✨")

#Role
with st.form("role_form"):
    if "role" not in st.session_state:
        st.session_state.role = None

    role = st.radio("Choisissez votre rôle :", ["Membre", "Membre de la cellule formation"])
    submitted_role = st.form_submit_button("Soumettre")

    if submitted_role:
        st.session_state.role = role


if st.session_state.role:

    if st.session_state.role == "Membre":
        st.subheader("Liste des formations disponibles. Veuillez choisir une formation pour s'inscrire!")

        trainings = {
            "Formation Communication": {
                "inscription": "https://forms.gle/6juyXrTtU98Kid3M9",
                "feedback": ""
            },
            "Formation Emotional Intelligence 1": {
                "inscription": "",
                "feedback": ""
            },
            "Formation Emotional Intelligence 2": {
                "inscription": "",
                "feedback": ""
            },
            "Formation Stoytelling": {
                "inscription": "",
                "feedback": ""
            },
            "Formation Teamwork": {
                "inscription": "",
                "feedback": ""
            },
            "Formation Negociation": {
                "inscription": "",
                "feedback": ""
            },
            "Formation Networking": {
                "inscription": "",
                "feedback": ""
            },
            "Formation Body Language": {
                "inscription": "",
                "feedback": ""
            },
            "Formation Leadership": {
                "inscription": "",
                "feedback": ""
            },
            "Formation Conflict Management": {
                "inscription": "",
                "feedback": ""
            },
            "Formation Speaking to inform & persuade": {
                "inscription": "",
                "feedback": ""
            },
            
        }

        choice = st.selectbox("Sélectionnez une formation", list(trainings.keys()))
        if choice:
            st.markdown(f"👉 [Lien d'inscription]({trainings[choice]['inscription']})")
            st.markdown(f"👉 [Lien de feedback]({trainings[choice]['feedback']})")

    # Membre de la cellule formation
    elif st.session_state.role == "Membre de la cellule formation":
        st.subheader("Découpage en groupes")

        # Session State for File & Members 
        if "uploaded_file" not in st.session_state:
            st.session_state.uploaded_file = None
        if "members_per_group" not in st.session_state:
            st.session_state.members_per_group = 5

        uploaded_file = st.file_uploader("Chargez la liste Excel des inscrits", type=["xlsx"])
        if uploaded_file is not None:
            st.session_state.uploaded_file = uploaded_file

        # Nombre de membres par groupe
        members_input = st.text_input(
            "Nombre de membres par groupe",
            value=str(st.session_state.get("members_per_group", 5))
        )

        # Valider le nombre
        try:
            members_per_group = int(members_input)
            if members_per_group < 1:
                st.error("Le nombre de membres doit être au moins 1.")
                members_per_group = None
        except ValueError:
            st.error("Veuillez entrer un nombre entier valide.")
            members_per_group = None

        if members_per_group:
            st.session_state.members_per_group = members_per_group

        if st.button("Soumettre les groupes"):
            if st.session_state.uploaded_file is None:
                st.error("Veuillez charger un fichier Excel.")
            elif not members_per_group:
                st.error("Veuillez entrer un nombre valide de membres par groupe.")
            else:
                df = pd.read_excel(st.session_state.uploaded_file)
                if "Nom et Prénom" not in df.columns:
                    st.error("La colonne 'Nom et Prénom' est introuvable dans le fichier.")
                else:
                    names = df["Nom et Prénom"].dropna().tolist()
                    random.shuffle(names)

                    # Calculate number of groups needed
                    groups = []
                    for i in range(0, len(names), members_per_group):
                        groups.append(names[i:i + members_per_group])


                    for idx, group in enumerate(groups, 1):
                        print(f"Groupe {idx}: {group}")

                    # Display each group as a table
                    for i, g in enumerate(groups, 1):
                        st.write(f"### Groupe {i}")
                        df_group = pd.DataFrame({"Nom et Prénom": g})
                        st.table(df_group)

                    # Prepare Excel for download
                    result = pd.DataFrame({f"Groupe {i+1}": pd.Series(g) for i, g in enumerate(groups)})
                    excel_buffer = BytesIO()
                    result.to_excel(excel_buffer, index=False, engine="openpyxl")
                    st.download_button(
                        label="📥 Télécharger les groupes en Excel",
                        data=excel_buffer.getvalue(),
                        file_name="groupes.xlsx"
                    )
