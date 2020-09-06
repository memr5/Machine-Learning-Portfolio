import numpy as np
import tensorflow as tf
import streamlit as st

file_name = "static/Names.txt"

with open(file_name,'r') as f:
    names = f.read().split("\n")[:-1]

MODEL = 'models/indian-baby-names-generator.h5'

num_rnn_units = 256
embedding_size = 16

tokens = [' ', '#', '-', '.', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
token_to_id = {' ': 0, '#': 1, '-': 2, '.': 3, 'A': 4, 'B': 5, 'C': 6, 'D': 7, 'E': 8, 'F': 9, 'G': 10, 'H': 11, 'I': 12, 'J': 13, 'K': 14, 'L': 15, 'M': 16, 'N': 17, 'O': 18, 'P': 19, 'Q': 20, 'R': 21, 'S': 22, 'T': 23, 'U': 24, 'V': 25, 'W': 26, 'X': 27, 'Y': 28, 'Z': 29, 'a': 30, 'b': 31, 'c': 32, 'd': 33, 'e': 34, 'f': 35, 'g': 36, 'h': 37, 'i': 38, 'j': 39, 'k': 40, 'l': 41, 'm': 42, 'n': 43, 'o': 44, 'p': 45, 'q': 46, 'r': 47, 's': 48, 't': 49, 'u': 50, 'v': 51, 'w': 52, 'x': 53, 'y': 54, 'z': 55}
n_tokens = len(token_to_id)
MAX_LENGTH = 11
start_token = ' '
pad_token = '#'

def getModel():
    model = tf.keras.models.Sequential()

    model.add(tf.keras.layers.Embedding(n_tokens,embedding_size,input_length=MAX_LENGTH))
    model.add(tf.keras.layers.SimpleRNN(num_rnn_units,return_sequences=True,activation='elu'))
    model.add(tf.keras.layers.SimpleRNN(num_rnn_units,return_sequences=True,activation='elu'))
    model.add(tf.keras.layers.Dense(n_tokens,activation='softmax'))
    
    model.load_weights(MODEL)

    return model


def generateName(model,seed_phrase=start_token,max_length=MAX_LENGTH):
    
    assert len(seed_phrase)<max_length, f"Length of the Seed-phrase is more than Max-Length: {max_length}"
    
    name = [seed_phrase]
    x = np.zeros((1,max_length),np.int32)

    x[0,0:len(seed_phrase)] = [token_to_id[token] for token in seed_phrase]
    
    for i in range(len(seed_phrase),max_length):       
        
        probs = list(model.predict(x)[0,i-1])
        
        probs = probs/np.sum(probs)
        
        index = np.random.choice(range(n_tokens),p=probs)
        
        if index == token_to_id[pad_token]:
            break
            
        x[0,i] = index
        
        name.append(tokens[index])
    
    return "".join(name)


st.set_option('deprecation.showfileUploaderEncoding', False)

st.markdown("""
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
            """,unsafe_allow_html=True)

st.markdown("""
<p align="center">
  <img width="400" height="400" src="https://media.giphy.com/media/TayI4SCiq0dJ6/giphy.gif">
</p>
""",unsafe_allow_html=True)

st.title("👶🏻 Indian Baby Names Generator")
# st.header("✍🏻 Generate New Indian Baby Names")

st.markdown("""[Kaggle Notebook](https://www.kaggle.com/meemr5/indian-baby-names-generator-text-processing-rnn/) | [Github](https://github.com/memr5/)""")

st.write("This is a text-generating web-app")

st.markdown("""
              <div class="container">
                <div class="alert alert-info">
                  <strong>Info!</strong> Length of the names generated will be upto 10 characters!
                </div>
              </div>
            """,unsafe_allow_html=True)

seed_phrase = str(st.text_input('Enter starting phrase',max_chars=9))

generate = st.button('Generate')

model = getModel()

if generate:
    text = None
    # st.text(seed_phrase)
    if seed_phrase == '':
        seed_phrase = ' '

    # st.text(seed_phrase)
    for char in seed_phrase:
        # st.text("Seed Phrase Check")
        # st.text(char)
        if char not in tokens:
            text = "Characters not supported"
            break
    
    if text is None:
        st.text("Generating New Names...")
        text = []
        while len(text)!=10:
            name = generateName(model,seed_phrase=seed_phrase).strip()
            if name not in names:
                # st.text(name)
                text.append(name)
        text = "\n".join(text)
    
    st.text(text)