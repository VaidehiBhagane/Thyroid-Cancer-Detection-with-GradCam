import logging, os
import keras
import tensorflow as tf
from huggingface_hub import hf_hub_download
from config import HF_REPO_ID, HF_MODEL_FILENAME

logger = logging.getLogger(__name__)

@keras.saving.register_keras_serializable()
class SEBlock(keras.layers.Layer):
    def __init__(self, ratio=16, **kwargs):
        super().__init__(**kwargs); self.ratio = ratio
    def build(self, input_shape):
        self.channels = input_shape[-1]
        self.global_pool = keras.layers.GlobalAveragePooling2D()
        self.fc1 = keras.layers.Dense(self.channels // self.ratio, activation='swish')
        self.fc2 = keras.layers.Dense(self.channels, activation='sigmoid')
        self.reshape = keras.layers.Reshape((1, 1, self.channels)); super().build(input_shape)
    def call(self, inputs):
        se = self.reshape(self.fc2(self.fc1(self.global_pool(inputs))))
        return inputs * se
    def get_config(self):
        config = super().get_config(); config.update({"ratio": self.ratio}); return config

@keras.saving.register_keras_serializable()
class Avg2MaxPooling(keras.layers.Layer):
    def __init__(self, pool_size=3, strides=2, padding='same', **kwargs):
        super().__init__(**kwargs)
        self.pool_size, self.strides, self.padding = pool_size, strides, padding
        self.avg_pool = keras.layers.AveragePooling2D(pool_size, strides, padding)
        self.max_pool = keras.layers.MaxPooling2D(pool_size, strides, padding)
        self.bn = keras.layers.BatchNormalization()
    def call(self, inputs):
        return self.bn(self.avg_pool(inputs) - 2 * self.max_pool(inputs))
    def get_config(self):
        config = super().get_config()
        config.update({"pool_size": self.pool_size, "strides": self.strides, "padding": self.padding})
        return config

@keras.saving.register_keras_serializable()
class DepthwiseSeparableConv(keras.layers.Layer):
    def __init__(self, filters, kernel_size=3, strides=1, se_ratio=16, reg=0.001, **kwargs):
        super().__init__(**kwargs)
        self.filters, self.kernel_size, self.strides, self.se_ratio, self.reg = filters, kernel_size, strides, se_ratio, reg
        self.dw = keras.layers.DepthwiseConv2D(kernel_size, strides, padding='same', depthwise_regularizer=keras.regularizers.l2(reg))
        self.pw = keras.layers.Conv2D(filters, 1, strides=1, kernel_regularizer=keras.regularizers.l2(reg))
        self.bn = keras.layers.BatchNormalization()
        self.se = SEBlock(se_ratio)
        self.proj = keras.layers.Conv2D(filters, 1, strides=1, kernel_regularizer=keras.regularizers.l2(reg)) if strides != 1 else None
    def call(self, inputs):
        residual = inputs; x = self.se(tf.nn.swish(self.bn(self.pw(self.dw(inputs)))))
        if self.proj is not None: residual = self.proj(residual)
        return x + residual if residual.shape == x.shape else x
    def get_config(self):
        config = super().get_config()
        config.update({"filters": self.filters, "kernel_size": self.kernel_size, "strides": self.strides, "se_ratio": self.se_ratio, "reg": self.reg})
        return config

def load_model():
    try:
        # Download model from HuggingFace Hub
        logger.info(f"Downloading model from HuggingFace: {HF_REPO_ID}/{HF_MODEL_FILENAME}")
        model_path = hf_hub_download(
            repo_id=HF_REPO_ID,
            filename=HF_MODEL_FILENAME,
            cache_dir="./model_cache"
        )
        logger.info(f"Model downloaded successfully to: {model_path}")
        
        # Verify file exists and is readable
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file '{model_path}' not found after download")
        if not os.access(model_path, os.R_OK):
            raise PermissionError(f"Cannot read model file '{model_path}'")
        
        # Load model with custom objects
        custom_objs = {"SEBlock": SEBlock, "Avg2MaxPooling": Avg2MaxPooling, "DepthwiseSeparableConv": DepthwiseSeparableConv}
        model = keras.saving.load_model(model_path, custom_objects=custom_objs, compile=False)
        
        if model is None or not hasattr(model, 'predict'):
            raise ValueError("Invalid model structure")
        
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        logger.info(f"Model loaded: {len(model.layers)} layers, {model.count_params()} params")
        return model
        
    except (FileNotFoundError, PermissionError, OSError, ValueError) as e:
        logger.error(f"Model loading failed: {str(e)}"); raise
    except KeyboardInterrupt:
        logger.warning("Loading interrupted"); raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise RuntimeError(f"Model loading failed: {str(e)}")
