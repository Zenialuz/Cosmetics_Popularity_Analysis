import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping

# -----------------------------
# CONFIGURACIÓN GENERAL
# -----------------------------
IMG_SIZE = (500, 500)  # Tamaño de las imágenes de entrada
BATCH_SIZE = 32
EPOCHS = 10
DATASET_PATH = 'images'
MODEL_PATH = 'models/skin_type_model.keras'
CLASS_INDICES_PATH = 'models/class_indices.npy'

# -----------------------------
# FUNCIÓN PARA ENTRENAR MODELO
# -----------------------------
def train_model():
    datagen = ImageDataGenerator(
        rescale=1./255,            # Normaliza los píxeles a [0,1]
        validation_split=0.2,      # Usa el 20% para validación. Se dividen en entrenamiento (80%) y validación (20%)
        horizontal_flip=True,      # Aumenta los datos con espejado horizontal
        zoom_range=0.2             # Aplica zoom aleatorio 
    )
    
    
    # Lee imágenes desde las subcarpetas de images/
    # Cada subcarpeta representa una clase. Se dividen en entrenamiento (80%) y validación (20%)
    train_generator = datagen.flow_from_directory(
        DATASET_PATH,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training'
    )

    val_generator = datagen.flow_from_directory(
        DATASET_PATH,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation'
    )
    # Definiendo la arquitectura del modelo CNN(convolucional)
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(*IMG_SIZE, 3)),  # Capas que detectan bordes, texturas, etc.
        MaxPooling2D(2, 2),  #Reduce la dimensión y conserva las características más importantes.
        Conv2D(64, (3, 3), activation='relu'),  
        MaxPooling2D(2, 2),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Flatten(), #Aplana la imagen a un vector para la red densa.
        Dropout(0.5),  # Ayuda a evitar overfitting.
        Dense(128, activation='relu'), # Capas totalmente conectadas. La última tiene tantas neuronas como clases
        Dense(len(train_generator.class_indices), activation='softmax')
    ])
    # Compilación del modelo
    model.compile(optimizer=Adam(),
                  loss='categorical_crossentropy',   # Porque la salida es categórica y one-hot
                  metrics=['accuracy'])
    # Entrenamiento del modelo con Early Stopping para evitar overfitting
    early_stop = EarlyStopping(monitor='val_loss', patience=3)

    model.fit(
        train_generator,
        epochs=EPOCHS,
        validation_data=val_generator,
        callbacks=[early_stop]
    )
    # Guardar el modelo entrenado en un archivo .keras
    # Verifica si la carpeta 'models' existe, si no, la crea
    if not os.path.exists('models'):
        os.makedirs('models')
        
    if os.path.exists(MODEL_PATH):
        os.remove(MODEL_PATH)
        
    # Guarda el modelo en la ruta especificada
    model.save(MODEL_PATH)
    print("Modelo guardado como", MODEL_PATH)

    if os.path.exists(CLASS_INDICES_PATH):
        os.remove(CLASS_INDICES_PATH)
       
        
    # se Guarda el índice de clases para usarlo luego en la predicción
    with open(CLASS_INDICES_PATH, "wb") as f:
        np.save(f, train_generator.class_indices)

# -----------------------------
# FUNCIÓN PARA HACER PREDICCIÓN
# -----------------------------
def predict_skin_type(image_path):
    # Cargar modelo y clases
    model = load_model(MODEL_PATH)
    class_indices = np.load(CLASS_INDICES_PATH, allow_pickle=True).item()
    class_labels = {v: k for k, v in class_indices.items()}

    # Preparar imagen
    img = load_img(image_path, target_size=IMG_SIZE)
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)
    predicted_class = np.argmax(prediction[0])
    skin_type = class_labels[predicted_class]

    return f"{skin_type}"


