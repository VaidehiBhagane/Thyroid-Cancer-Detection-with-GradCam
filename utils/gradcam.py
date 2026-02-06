import tensorflow as tf
import numpy as np
import logging

logger = logging.getLogger(__name__)

# --------------------------------------------------
# Grad-CAM Interpretability Function
# --------------------------------------------------
def make_gradcam_heatmap(img_array, model, last_conv_layer_name, pred_index=None):
    """
    Generate Grad-CAM heatmap for model interpretability.
    
    Args:
        img_array: Preprocessed image array
        model: Trained model
        last_conv_layer_name: Name of the last convolutional layer
        pred_index: Target class index (None = predicted class)
    
    Returns:
        Heatmap as numpy array
    """
    try:
        # Create a model that returns the conv layer output and final predictions
        grad_model = tf.keras.models.Model(
            inputs=[model.inputs],
            outputs=[model.get_layer(last_conv_layer_name).output, model.output]
        )

        # Compute gradients
        with tf.GradientTape() as tape:
            conv_outputs, predictions = grad_model(img_array)
            
            # Get the predicted class if not specified
            if pred_index is None:
                # For binary classification, use the sigmoid output directly
                pred_value = predictions[0].numpy()[0]
                pred_index = 1 if pred_value >= 0.5 else 0
            
            # Get the class output (for binary: predictions[0, 0])
            class_output = predictions[0][0]

        # Compute gradients of the class output with respect to the conv layer output
        grads = tape.gradient(class_output, conv_outputs)
        
        # Global average pooling on the gradients
        # Shape: (batch, height, width, channels) -> (channels,)
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        
        # Convert to numpy
        conv_outputs_np = conv_outputs.numpy()[0]  # Remove batch dimension
        pooled_grads_np = pooled_grads.numpy()
        
        # Ensure they have compatible shapes
        logger.info(f"Conv output shape: {conv_outputs_np.shape}, Pooled grads shape: {pooled_grads_np.shape}")
        
        # Weight each channel by its importance
        # conv_outputs_np shape: (H, W, C)
        # pooled_grads_np shape: (C,)
        # Broadcasting will handle this correctly
        for i in range(pooled_grads_np.shape[0]):
            conv_outputs_np[:, :, i] *= pooled_grads_np[i]
        
        # Average across all channels to get the heatmap
        heatmap = np.mean(conv_outputs_np, axis=-1)
        
        # Apply ReLU to heatmap
        heatmap = np.maximum(heatmap, 0)
        
        # Normalize the heatmap
        if np.max(heatmap) > 0:
            heatmap = heatmap / np.max(heatmap)
        
        return heatmap
        
    except Exception as e:
        logger.error(f"Error in make_gradcam_heatmap: {str(e)}", exc_info=True)
        raise
