import streamlit as st
import pandas as pd

def cifra_cesar(texto, deslocamento):
    """Aplica a Cifra de César em um texto"""
    resultado = ""
    for char in texto:
        if char.isalpha():
            ascii_base = ord('A') if char.isupper() else ord('a')
            novo_char = chr((ord(char) - ascii_base + deslocamento) % 26 + ascii_base)
            resultado += novo_char
        else:
            resultado += char
    return resultado

def deslocamento_aprox(x):
    if x < 7:
        return 'Entre 1 e 6'
    elif x < 15:
        return 'Entre 7 e 14'
    else: 
        return 'Entre 14 e 26'

def main_grid():
    st.title("🔐 Cifra de César - Grid Interativo")
    st.markdown("### Controle individual para cada palavra!")
    
    # Inicializar session_state se não existir
    if 'resultados' not in st.session_state:
        st.session_state.resultados = None
    if 'num_palavras' not in st.session_state:
        st.session_state.num_palavras = 4
    if 'criptografia_executada' not in st.session_state:
        st.session_state.criptografia_executada = False
    
    num_palavras = st.slider("Número de palavras", 1, 10, st.session_state.num_palavras)
    st.session_state.num_palavras = num_palavras
    
    st.subheader("🎛️ Configuração das Palavras")
    
    # Criar grid dinâmico
    col1, col2, col3 = st.columns([3, 2, 2])
    
    with col1:
        st.markdown("**Palavra**")
    with col2:
        st.markdown("**Deslocamento**")
    with col3:
        st.markdown("**Pré-visualização**")
    
    palavras_config = []
    
    for i in range(num_palavras):
        col1, col2, col3 = st.columns([3, 2, 2])
        
        with col1:
            palavra = st.text_input(
                f"Palavra {i+1}",
                key=f"text_{i}",
                placeholder="Digite aqui...",
                label_visibility="collapsed"
            )
        
        with col2:
            deslocamento = st.slider(
                f"Desl. {i+1}",
                min_value=1,
                max_value=25,
                value=(i * 2) % 25 + 1,
                key=f"slider_{i}",
                label_visibility="collapsed"
            )
        
        with col3:
            if palavra:
                cripto = cifra_cesar(palavra, deslocamento)
                st.code(f"{cripto}", language="text")
            else:
                st.write("⏳")
        
        if palavra:
            palavras_config.append((palavra, deslocamento))
    
    # Botão de ação
    if st.button("🎯 Executar Criptografia Completa", type="primary"):
        if len(palavras_config) == num_palavras:
            
            # Processar resultados
            resultados = []
            for palavra, deslocamento in palavras_config:
                cripto = cifra_cesar(palavra, deslocamento)
                resultados.append({
                    'Palavra': palavra,
                    'Deslocamento': deslocamento,
                    'Criptografada': cripto
                })
            
            # Salvar resultados no session_state
            st.session_state.resultados = resultados
            st.session_state.criptografia_executada = True
            
            # Recarregar a página para mostrar os resultados
            st.rerun()
    
    # Exibir resultados se a criptografia foi executada
    if st.session_state.criptografia_executada and st.session_state.resultados:
        st.success("✅ Criptografia concluída!")
        
        # Frase completa
        frase_original = " ".join([r['Palavra'] for r in st.session_state.resultados])
        frase_cripto = " ".join([r['Criptografada'] for r in st.session_state.resultados])
        
        st.metric("Frase Criptografada", frase_cripto, border=True)
        
        st.markdown("### 🎮 Tente Adivinhar as Palavras")
        
        # Contador de acertos
        acertos = 0
        
        for i in range(len(st.session_state.resultados)):
            game1, game2, game3, game4 = st.columns([2, 2, 2, 1])
            
            with game1:
                st.markdown("**Palavra Criptografada**")
                st.code(st.session_state.resultados[i]['Criptografada'])
            
            with game2:
                st.markdown("**Sua Resposta**")
                # Usar um key único para cada campo de resposta
                palavra_resposta = st.text_input(
                    f"Digite a palavra original {i+1}",
                    key=f"resposta_{i}",
                    placeholder="Digite aqui...",
                    label_visibility="collapsed"
                )
            
            with game3:
                st.markdown("**Resultado**")
                if palavra_resposta:
                    if palavra_resposta.lower() == st.session_state.resultados[i]['Palavra'].lower():
                        st.success(f"✅ {st.session_state.resultados[i]['Palavra']}")
                        acertos += 1
                    else:
                        st.error("❌ Tente novamente")
                else:
                    st.info("⏳ Aguardando resposta")

            with game4:
                st.markdown("**Dicas**")
                with st.popover("Dicas"):
                    dica1 = st.checkbox("Dica 1", key=f"dica_1_{i}")
                    dica2 = st.checkbox("Dica 2", key=f"dica_2_{i}")

                    if dica1:
                        st.write(f"1° letra: {st.session_state.resultados[i]['Palavra'][0].lower()}")
                    if dica2:
                        st.write(f"Deslocamento: {deslocamento_aprox(st.session_state.resultados[i]['Deslocamento'])}")
        
        # Mostrar progresso
        if acertos > 0:
            st.progress(acertos / len(st.session_state.resultados))
            st.write(f"🎯 {acertos} de {len(st.session_state.resultados)} corretas")
            
            if acertos == len(st.session_state.resultados):
                st.balloons()
                st.success("🎉 Parabéns! Você decifrou todas as palavras!")
        
        # Botão para reiniciar
        if st.button("🔄 Nova Criptografia"):
            st.session_state.criptografia_executada = False
            st.session_state.resultados = None
            for i in range(len(st.session_state.resultados) if st.session_state.resultados else 0):
                if f"resposta_{i}" in st.session_state:
                    del st.session_state[f"resposta_{i}"]
            st.rerun()

if __name__ == "__main__":
    main_grid()