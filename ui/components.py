import streamlit as st
import pandas as pd

def setup_page():
    st.set_page_config(
        page_title="Smart Garbage Classifier App",
        page_icon="♻️",
        layout="wide"
    )

def display_sidebar(frame_interval_option=False):
    with st.sidebar:
        st.title("⚙️ Options")
        st.markdown("Configure the input and prediction settings.")

        input_method = st.radio(
            "Select Input Method:",
            ("Upload Image", "Image URL", "Upload Video"),
            key="input_method_radio"
        )

        confidence_threshold = st.slider(
            "Minimum Confidence Threshold (%)", 0, 100, 50, 5, key="confidence_slider"
        )

        frame_interval_secs = None
        if frame_interval_option and input_method == "Upload Video":
            frame_interval_secs = st.slider(
                "Process Frame Every X Seconds:", 0.5, 10.0, 2.0, 0.5,
                key="frame_interval_slider",
                help="Higher values process fewer frames (faster), lower values are more thorough (slower)."
            )

        return input_method, confidence_threshold, frame_interval_secs

def display_model_info(model_path, target_size, expected_class_names, class_info):
    with st.sidebar:
        with st.expander("ℹ️ Model Information"):
            st.write(f"**Model Path:** `{model_path.name}`")
            st.write(f"**Expected Input Size:** {target_size}")
            st.write(f"**Number of Classes:** {len(expected_class_names)}")
            st.write("**Classes:**")
            for name in expected_class_names:
                st.write(f"- {class_info[name]['display_name']}")

def display_prediction(prediction_probs, class_info_dict, expected_class_names, confidence_threshold, prefix=""):
    predicted_index = prediction_probs.argmax()
    confidence = prediction_probs.max() * 100

    if confidence >= confidence_threshold:
        if predicted_index < len(expected_class_names):
            predicted_class_key = expected_class_names[predicted_index]
            info = class_info_dict.get(predicted_class_key, class_info_dict['unknown'])
        else:
            info = class_info_dict['unknown']
            predicted_class_key = 'unknown'
    else:
        info = class_info_dict['unknown']
        predicted_class_key = 'unknown'

    st.subheader(f"{prefix}📊 Classification Result")
    box_color = info.get('color', '#BDBDBD')
    result_style = f"""
        <div style="border: 1px solid {box_color}; border-left: 5px solid {box_color}; border-radius: 5px; padding: 15px; margin-bottom: 15px; background-color: #f9f9f9;">
            <p style="font-size: 22px; font-weight: bold; color: {box_color}; margin-bottom: 5px;">
                {info.get('icon', '')} {info.get('display_name', 'N/A')}
            </p>
            <p style="font-size: 14px; margin-bottom: 10px;">{info.get('description', '')}</p>
            <hr style="border-top: 1px solid #eee; margin-top: 10px; margin-bottom: 10px;">
            <p style="font-size: 16px;">Confidence: <strong>{confidence:.2f}%</strong></p>
            <p style="font-size: 14px;">Recyclable: <strong>{info.get('recyclable', 'N/A')}</strong></p>
            <p style="font-size: 14px;"><strong>Handling:</strong> {info.get('handling', '')}</p>
        </div>
    """
    st.markdown(result_style, unsafe_allow_html=True)
    return predicted_class_key, confidence

def display_probability_details(prediction_probs, expected_class_names, class_info):
    with st.expander("🔬 View Detailed Probabilities"):
        prob_data = {
            'Class': [class_info[name]['display_name'] for name in expected_class_names],
            'Probability': prediction_probs
        }
        prob_df = pd.DataFrame(prob_data)
        prob_df = prob_df.sort_values(by='Probability', ascending=False)
        prob_df['Probability'] = prob_df['Probability'].apply(lambda x: f"{x*100:.2f}%")
        st.dataframe(prob_df, use_container_width=True, hide_index=True)

def display_video_results(video_results):
    if video_results:
        df_results = pd.DataFrame(video_results)
        valid_predictions = df_results[df_results['Class Key'] != 'unknown']

        if not valid_predictions.empty:
            prediction_counts = valid_predictions['Predicted Class'].value_counts()
            most_frequent_class = prediction_counts.index[0]
            count = prediction_counts.iloc[0]

            st.metric(
                label="Most Frequent Prediction (above threshold)",
                value=most_frequent_class,
                delta=f"{count} frames",
                delta_color="off"
            )
        else:
            st.info("No classifications were made above the confidence threshold.")

        with st.expander("🔬 View Frame-by-Frame Details"):
            st.dataframe(df_results[['Timestamp (s)', 'Predicted Class', 'Confidence (%)']], 
                         use_container_width=True, hide_index=True)
    else:
        st.info("No frames were processed or no results generated.")