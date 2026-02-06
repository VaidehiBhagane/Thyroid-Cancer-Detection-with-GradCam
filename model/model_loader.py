import streamlit as st
import logging
import keras
import tensorflow as tf

logger = logging.getLogger(__name__)

# Recreate EXACT custom layers from training script
# Moving these to module level so they are pickleable and accessible
@keras.saving.register_keras_serializable()
class SEBlock(keras.layers.Layer):
    def __init__(self, ratio=16, **kwargs):
        super().__init__(**kwargs)
        self.ratio = ratio
    
    def build(self, input_shape):
        self.channels = input_shape[-1]
        self.global_pool = keras.layers.GlobalAveragePooling2D()
        self.fc1 = keras.layers.Dense(self.channels // self.ratio, activation='swish')
        self.fc2 = keras.layers.Dense(self.channels, activation='sigmoid')
        self.reshape = keras.layers.Reshape((1, 1, self.channels))
        super().build(input_shape)
    
    def call(self, inputs):
        se = self.global_pool(inputs)
        se = self.fc1(se)
        se = self.fc2(se)
        se = self.reshape(se)
        return inputs * se
    
    def get_config(self):
        config = super().get_config()
        config.update({"ratio": self.ratio})
        return config

@keras.saving.register_keras_serializable()
class Avg2MaxPooling(keras.layers.Layer):
    def __init__(self, pool_size=3, strides=2, padding='same', **kwargs):
        super().__init__(**kwargs)
        self.pool_size = pool_size
        self.strides = strides
        self.padding = padding
        self.avg_pool = keras.layers.AveragePooling2D(pool_size, strides, padding)
        self.max_pool = keras.layers.MaxPooling2D(pool_size, strides, padding)
        self.bn = keras.layers.BatchNormalization()
    
    def call(self, inputs):
        x = self.avg_pool(inputs) - 2 * self.max_pool(inputs)
        return self.bn(x)
    
    def get_config(self):
        config = super().get_config()
        config.update({
            "pool_size": self.pool_size,
            "strides": self.strides,
            "padding": self.padding
        })
        return config

@keras.saving.register_keras_serializable()
class DepthwiseSeparableConv(keras.layers.Layer):
    def __init__(self, filters, kernel_size=3, strides=1, se_ratio=16, reg=0.001, **kwargs):
        super().__init__(**kwargs)
        self.filters = filters
        self.kernel_size = kernel_size
        self.strides = strides
        self.se_ratio = se_ratio
        self.reg = reg
        self.dw = keras.layers.DepthwiseConv2D(
            kernel_size, strides, padding='same',
            depthwise_regularizer=keras.regularizers.l2(reg)
        )
        self.pw = keras.layers.Conv2D(
            filters, 1, strides=1,
            kernel_regularizer=keras.regularizers.l2(reg)
        )
        self.bn = keras.layers.BatchNormalization()
        self.se = SEBlock(se_ratio)
        self.proj = keras.layers.Conv2D(
            filters, 1, strides=1,
            kernel_regularizer=keras.regularizers.l2(reg)
        ) if strides != 1 else None
    
    def call(self, inputs):
        residual = inputs
        x = self.dw(inputs)
        x = self.pw(x)
        x = self.bn(x)
        x = tf.nn.swish(x)
        x = self.se(x)
        if self.proj is not None:
            residual = self.proj(residual)
        return x + residual if residual.shape == x.shape else x
    
    def get_config(self):
        config = super().get_config()
        config.update({
            "filters": self.filters,
            "kernel_size": self.kernel_size,
            "strides": self.strides,
            "se_ratio": self.se_ratio,
            "reg": self.reg
        })
        return config

# --------------------------------------------------
# Load model
# --------------------------------------------------
@st.cache_resource
def load_model():
    """Load the pre-trained thyroid cancer detection model."""
    try:
        logger.info("Loading thyroid cancer model...")
        
        # Custom objects mapping
        custom_objs = {
            "SEBlock": SEBlock,
            "Avg2MaxPooling": Avg2MaxPooling,
            "DepthwiseSeparableConv": DepthwiseSeparableConv,
        }
        
        # Load model
        model = keras.saving.load_model(
            "thyroid_cancer_model.h5",
            custom_objects=custom_objs,
            compile=False
        )
        
        logger.info("Model loaded successfully")
        
        # Compile the model
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        logger.info("Model compiled")
        
        logger.info(f"Model input shape: {model.input_shape}")
        logger.info(f"Model output shape: {model.output_shape}")
        logger.info(f"Total layers: {len(model.layers)}")
        return model
    
    except FileNotFoundError:
        logger.error("Model file 'thyroid_cancer_model.h5' not found")
        st.error("❌ Model file not found. Please ensure 'thyroid_cancer_model.h5' is in the project directory.")
        st.stop()
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        st.error(f"❌ Failed to load model: {str(e)}")
        st.stop()
