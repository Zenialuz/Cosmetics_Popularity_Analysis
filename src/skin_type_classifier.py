import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping

# -----------------------------
# CONFIGURACIÓN GENERAL
# -----------------------------
IMG_SIZE = (224, 224)  # Tamaño recomendado para MobileNetV2
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
        preprocessing_function=preprocess_input,  # Preprocesamiento de MobileNetV2
        validation_split=0.2,                     # Usa el 20% para validación. Se dividen en entrenamiento (80%) y validación (20%)
        horizontal_flip=True,                     # Aumenta los datos con espejado horizontal
        zoom_range=0.2                            # Aplica zoom aleatorio a las imágenes
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

    # Cargar MobileNetV2 como base del modelo
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(*IMG_SIZE, 3))
    base_model.trainable = False  # No entrenar la base preentrenada

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dropout(0.5)(x)
    x = Dense(128, activation='relu')(x)
    predictions = Dense(len(train_generator.class_indices), activation='softmax')(x)

    model = Model(inputs=base_model.input, outputs=predictions)

    model.compile(optimizer=Adam(),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    early_stop = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

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

    model.save(MODEL_PATH)
    print("Modelo guardado como", MODEL_PATH)

    # se Guarda el índice de clases para usarlo luego en la predicción
    if os.path.exists(CLASS_INDICES_PATH):
        os.remove(CLASS_INDICES_PATH)

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
    img_array = img_to_array(img)
    img_array = preprocess_input(img_array)  # Preprocesamiento específico de MobileNetV2
    img_array = np.expand_dims(img_array, axis=0)

    # Realizar predicción
    prediction = model.predict(img_array)
    predicted_class = np.argmax(prediction[0])
    skin_type = class_labels[predicted_class]

    return f"{skin_type}"
