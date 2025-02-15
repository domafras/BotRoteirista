import streamlit as st
from PIL import Image
import inteligencia

st.set_page_config(layout="wide") #centered
chave = st.secrets["GEMINI_CHAVE"]

st.title(":rainbow[BotRoteirista]")
st.subheader("O seu assistente virtual para criar roteiros!")

col1, col2 = st.columns([2,2])

with col1:
    st.header("Faça o upload de uma foto dos seus produtos")
    
    opcao_entrada = st.radio(
        "Escolha como deseja adicionar a foto:",
        ["Upload de arquivo", "Tirar foto"],
        horizontal=True
    )
    
    if opcao_entrada == "Upload de arquivo":
        arquivo_foto = st.file_uploader(" ", type=["jpg", "jpeg", "png"])
    else:
        arquivo_foto = st.camera_input(" ")
        
    if arquivo_foto is not None:
        imagem = Image.open(arquivo_foto)
        st.image(imagem)
        with st.spinner("Pensando..."):
            if st.button("Identificar produtos"):
                st.session_state.produtos = inteligencia.detectar_produtos(chave, imagem)
                st.session_state.roteiros = inteligencia.possiveis_roteiros(chave, st.session_state.produtos)

    if 'produtos' in st.session_state:
        st.write(f"Produtos identificados: {st.session_state.produtos}")
        st.write(":rainbow[Ideias de roteiro:]")
        for id, roteiro in enumerate(st.session_state.roteiros, start=1):
            st.write(f"{id}. {roteiro}")

with col2:
    if 'roteiros' in st.session_state:
        st.header("Selecione o roteiro")
        roteiro_selecionado = st.selectbox("Tema do vídeo", st.session_state.roteiros)
        
        estilo = st.selectbox(
            'Estilo do roteiro',
            ['Informal', 'Divertido', 'Informativo', 'Publi']
        )
        
        with st.spinner("Gerando..."):
            if st.button("Gerar roteiro"):
                st.session_state.roteiro_completo = inteligencia.roteiro_completo(chave, 
                                                                            st.session_state.produtos, 
                                                                            roteiro_selecionado, 
                                                                            estilo)
                st.write(st.session_state.roteiro_completo)