import numpy as np
import tensorflow as tf
from keras import models
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from dataset import dataset as dataset



queries = [data["query"] for data in dataset]
responses = [data["response"] for data in dataset]


# Assuming 'responses' is your NumPy array containing responses
response_indices = [np.where(responses == response)[0][0] for response in responses]



# Tokenize the queries
tokenizer = Tokenizer()
tokenizer.fit_on_texts(queries)
word_index = tokenizer.word_index
sequences = tokenizer.texts_to_sequences(queries)
max_sequence_length = max([len(seq) for seq in sequences])
padded_sequences = pad_sequences(sequences, maxlen=max_sequence_length, padding='post')

# Convert responses to numpy array
responses = np.array(responses)

# Convert responses to indices
response_indices = [responses.index(response) for response in responses]

# Define and compile the model
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(len(word_index) + 1, 64, input_length=max_sequence_length),
    tf.keras.layers.LSTM(128),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')  # Use binary classification for simplicity
])

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
model.fit(padded_sequences, np.array(response_indices), epochs=10)

# Save the model for later use
model.save("alfred_model.h5")