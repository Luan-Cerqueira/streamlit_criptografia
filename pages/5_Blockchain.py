import streamlit as st
import hashlib
import datetime as date

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        hash_string = str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)
        return hashlib.sha256(hash_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, date.datetime.now(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

# Inicializa a blockchain na sessão do Streamlit
if 'blockchain' not in st.session_state:
    st.session_state.blockchain = Blockchain()

st.title('Simulador de Blockchain em Python')
st.markdown('---')

## Adicionar uma nova transação
st.header('Adicionar uma Nova Transação')
transaction_data = st.text_area("Insira os dados da transação (ex: De: A, Para: B, Quantia: 10):", height=100)
if st.button('Adicionar Transação'):
    if transaction_data:
        latest_block = st.session_state.blockchain.get_latest_block()
        new_block = Block(
            index=latest_block.index + 1,
            timestamp=date.datetime.now(),
            data=transaction_data,
            previous_hash=latest_block.hash
        )
        st.session_state.blockchain.add_block(new_block)
        st.success('Transação adicionada com sucesso! 🎉')
        st.rerun()  # Recarrega a página para mostrar a cadeia atualizada
    else:
        st.warning('Por favor, insira os dados da transação.')

st.markdown('---')

## Visualizar a Blockchain
st.header('Cadeia de Blocos Atual')
for block in st.session_state.blockchain.chain:
    with st.expander(f"Bloco #{block.index}"):
        st.json({
            "index": block.index,
            "timestamp": str(block.timestamp),
            "data": block.data,
            "previous_hash": block.previous_hash,
            "hash": block.hash
        })

if st.session_state.blockchain.is_valid():
    st.sidebar.success('✅ A blockchain é válida.')
else:

    st.sidebar.error('⚠️ A blockchain não é válida!')