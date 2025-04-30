from sklearn.model_selection import train_test_split
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
import pandas as pd

input_dim = 4
output_dim = 4
num_epochs = 3000

# Define the neural network architecture
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='softsign', input_shape=(input_dim,)), # Input layer with 64 neurons and ReLU activation
    tf.keras.layers.Dense(32, activation='softsign'), # Hidden layer with 32 neurons and ReLU activation
    tf.keras.layers.Dense(output_dim) # Output layer
])

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])

# Print a summary of the model architecture
#model.summary()

#read the dataset in
df = pd.read_csv('./dataset.csv',encoding='utf-8')
#print(df.head())

#make x the data and y the target
x = df.iloc[0:,:4].values
y = df.iloc[0:, 4:].values

#print(x[0])
#print(y[0])

#split dataset into training and testing dataset
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3,random_state=109) # 70% training and 30% test

# Train the model
history = model.fit(x_train, y_train, epochs=num_epochs)

# Evaluate the model
loss, accuracy = model.evaluate(x_test, y_test)

# Print the evaluation results
print(f'Test Loss: {loss}')
print(f'Test Accuracy: {accuracy}')

#model.save("./src/model/py_model.keras")