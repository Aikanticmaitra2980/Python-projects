from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.optimizers import Adam
# Create a simple neural network model
model = keras.Sequential([
    layers.Dense(16, activation='relu', input_shape=(4,)),  # Input layer (example: 4 features)
    layers.Dense(8, activation='relu'),                     # Hidden layer
    layers.Dense(3, activation='softmax')                   # Output layer (example: 3 classes)
])

# Compile the model
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# To train the model, use:
# model.fit(X_train, y_train, epochs=10, batch_size=32)

# To see the model summary:
model.summary()