import streamlit as st
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
import pickle
import numpy as np

# Load the pre-trained LSTM model and tokenizer
model = load_model('spam_classifier_model.h5')
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

# Function to preprocess text and make predictions
def classify_message(message):
    max_len = 150  # Same as during training
    sequence = tokenizer.texts_to_sequences([message])
    padded_sequence = pad_sequences(sequence, maxlen=max_len)
    prediction = model.predict(padded_sequence)
    return prediction[0][0]  # Assuming model outputs a single probability score

# Function to check for fraud characteristics in the message
def check_fraud_indicators(message):
    fraud_indicators = [
        "bank", "nomor", "kartu kredit", "kata sandi", "nomor rekening",
        "data","diri", "pribadi", "klaim", "senilai","dinonaktifkan","pemenang","terpilih","mencurigakan",
        "penawaran terlalu bagus", "diskon besar", "kesempatan investasi","dibatasi","aktivitas","permanen","tunai"
        "tekanan waktu", "bertindak segera", "akun Anda dalam bahaya", "kesalahan tatabahasa", "ejaan yang mencurigakan", "identitas", "institusi terkemuka",
        "lampiran", "file unduhan",
    ]
    for indicator in fraud_indicators:
        if indicator in message.lower():
            return True
    return False

# Streamlit app
st.title('DETEKSI SPAM PENIPUAN')
user_input = st.text_area("Masukkan sebuah pesan:")

if st.button('Cek'):
    prediction_score = classify_message(user_input)
    is_fraud = check_fraud_indicators(user_input)
    
    if prediction_score > 0.5:
        if is_fraud:
            st.error("Pesan ini adalah spam penipuan")
            st.write(f"Accuracy: {np.max(prediction_score) * 100:.2f}%")
        else:
            st.warning("Pesan ini adalah spam biasa")
            st.write(f"Accuracy: {np.max(prediction_score) * 100:.2f}%")
    else:
        st.success("Pesan ini adalah ham (bukan spam)")
        st.write(f"Accuracy: {np.max(prediction_score) * 100:.2f}%")
    
    # Displaying the prediction confidence
    # st.write(f"Accuracy: {np.max(prediction_score) * 100:.2f}%")