import tensorflow as tf
from tensorflow.keras.layers import (
    LSTM as OriginalLSTM, Layer, AveragePooling2D, MaxPooling2D, 
    DepthwiseConv2D, Conv2D
)

# --------------------------------------------------
# Custom LSTM (same fix as heart murmur project)
# --------------------------------------------------
class CustomLSTM(OriginalLSTM):
    def __init__(self, *args, **kwargs):
        kwargs.pop("time_major", None)
        super().__init__(*args, **kwargs)

# --------------------------------------------------
# Custom Avg2MaxPooling Layer
# --------------------------------------------------
class Avg2MaxPooling(Layer):
    def __init__(self, pool_size=(2, 2), **kwargs):
        super(Avg2MaxPooling, self).__init__(**kwargs)
        self.pool_size = pool_size
        self.avg_pool = AveragePooling2D(pool_size=pool_size)
        self.max_pool = MaxPooling2D(pool_size=pool_size)
    
    def call(self, inputs):
        avg = self.avg_pool(inputs)
        max_val = self.max_pool(inputs)
        return (avg + max_val) / 2.0
    
    def get_config(self):
        config = super(Avg2MaxPooling, self).get_config()
        config.update({"pool_size": self.pool_size})
        return config

# --------------------------------------------------
# Custom DepthwiseSeparableConv Layer
# --------------------------------------------------
# Must recreate the exact structure with depthwise_conv and pointwise_conv sublayers
class DepthwiseSeparableConv(Layer):
    def __init__(self, filters, kernel_size=(3, 3), strides=(1, 1), padding='same', reg=0.0, **kwargs):
        super(DepthwiseSeparableConv, self).__init__(**kwargs)
        self.filters = filters
        self.kernel_size = kernel_size if isinstance(kernel_size, (list, tuple)) else (kernel_size, kernel_size)
        self.strides = strides if isinstance(strides, (list, tuple)) else (strides, strides)
        self.padding = padding
        self.reg = reg
        regularizer = tf.keras.regularizers.l2(reg) if reg > 0 else None
        
        # Create sublayers in __init__ so they're properly tracked
        self.depthwise_conv = DepthwiseConv2D(
            kernel_size=self.kernel_size,
            strides=self.strides,
            padding=self.padding,
            depthwise_regularizer=regularizer
        )
        self.pointwise_conv = Conv2D(
            self.filters,
            kernel_size=(1, 1),
            padding='same',
            kernel_regularizer=regularizer
        )
    
    def call(self, inputs):
        x = self.depthwise_conv(inputs)
        x = self.pointwise_conv(x)
        return x
    
    def get_config(self):
        config = super(DepthwiseSeparableConv, self).get_config()
        config.update({
            "filters": self.filters,
            "kernel_size": self.kernel_size,
            "strides": self.strides,
            "padding": self.padding,
            "reg": self.reg
        })
        return config
    
    @classmethod  
    def from_config(cls, config):
        return cls(**config)
