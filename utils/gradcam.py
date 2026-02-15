import tensorflow as tf
import numpy as np
import logging

logger = logging.getLogger(__name__)

def make_gradcam_heatmap(img_array, model, last_conv_layer_name, pred_index=None):
    try:
        if img_array is None or model is None or not last_conv_layer_name:
            raise ValueError("Invalid inputs: image, model, or layer name is None/empty")
        if len(img_array.shape) != 4:
            raise ValueError(f"Expected 4D array, got shape: {img_array.shape}")
        try:
            conv_layer = model.get_layer(last_conv_layer_name)
        except ValueError:
            available = [l.name for l in model.layers]
            raise ValueError(f"Layer '{last_conv_layer_name}' not found. Available: {available[:10]}...")
        grad_model = tf.keras.models.Model(inputs=[model.inputs], outputs=[conv_layer.output, model.output])
        with tf.GradientTape() as tape:
            conv_outputs, predictions = grad_model(img_array)
            if conv_outputs is None or predictions is None:
                raise RuntimeError("Model returned None outputs")
            if pred_index is None:
                # Handle model output - predictions is a tensor
                pred_tensor = predictions[0] if isinstance(predictions, list) else predictions
                pred_value = float(pred_tensor.numpy()[0][0])
                pred_index = 1 if pred_value >= 0.5 else 0
                logger.info(f"Predicted class: {pred_index} (confidence: {pred_value:.4f})")
            # Use the raw tensor for gradient computation
            pred_tensor = predictions[0] if isinstance(predictions, list) else predictions
            class_output = pred_tensor[:, 0]
        grads = tape.gradient(class_output, conv_outputs)
        if grads is None:
            raise RuntimeError("Gradient computation failed")
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        conv_outputs_np = conv_outputs.numpy()[0]
        pooled_grads_np = pooled_grads.numpy()
        if conv_outputs_np.shape[-1] != pooled_grads_np.shape[0]:
            raise ValueError(f"Shape mismatch: {conv_outputs_np.shape[-1]} != {pooled_grads_np.shape[0]}")
        for i in range(pooled_grads_np.shape[0]):
            conv_outputs_np[:, :, i] *= pooled_grads_np[i]
        heatmap = np.maximum(np.mean(conv_outputs_np, axis=-1), 0)
        heatmap_max = np.max(heatmap)
        if heatmap_max > 0:
            heatmap = heatmap / heatmap_max
        else:
            logger.warning("Heatmap all zeros")
        if np.isnan(heatmap).any() or np.isinf(heatmap).any():
            raise RuntimeError("Heatmap contains NaN/Inf values")
        logger.info(f"Heatmap generated: {heatmap.shape}")
        return heatmap
    except (ValueError, RuntimeError) as e:
        logger.error(f"Grad-CAM failed: {str(e)}"); raise
    except KeyboardInterrupt:
        logger.warning("Interrupted"); raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise RuntimeError(f"Grad-CAM failed: {str(e)}")
