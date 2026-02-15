from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from io import BytesIO
import base64, logging
from datetime import datetime

logger = logging.getLogger(__name__)

def generate_pdf_report(prediction_data: dict, gradcam_data: dict = None) -> BytesIO:
    try:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        elements = []; styles = getSampleStyleSheet()
        title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=24, textColor=colors.HexColor('#0066CC'), spaceAfter=30, alignment=TA_CENTER, fontName='Helvetica-Bold')
        heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading2'], fontSize=16, textColor=colors.HexColor('#333333'), spaceAfter=12, spaceBefore=12, fontName='Helvetica-Bold')
        normal_style = ParagraphStyle('CustomNormal', parent=styles['Normal'], fontSize=11, spaceAfter=12, alignment=TA_LEFT)
        elements.append(Paragraph(" Thyroid Cancer Detection Report", title_style))
        elements.append(Spacer(1, 0.2 * inch))
        timestamp = prediction_data.get('timestamp', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        filename = prediction_data.get('filename', 'Unknown')
        metadata_table = Table([['Report Generated:', timestamp], ['Image Filename:', filename], ['Report Type:', 'AI-Assisted Analysis']], colWidths=[2*inch, 4*inch])
        metadata_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F3F4F6')), ('TEXTCOLOR', (0, 0), (-1, -1), colors.black), ('ALIGN', (0, 0), (-1, -1), 'LEFT'), ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'), ('FONTNAME', (1, 0), (1, -1), 'Helvetica'), ('FONTSIZE', (0, 0), (-1, -1), 10), ('BOTTOMPADDING', (0, 0), (-1, -1), 8), ('TOPPADDING', (0, 0), (-1, -1), 8), ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)]))
        elements.append(metadata_table)
        elements.append(Spacer(1, 0.3 * inch))
        elements.append(Paragraph("Prediction Results", heading_style))
        prediction = prediction_data.get('prediction', {})
        pred_class = prediction.get('class', 'N/A'); pred_label = prediction.get('label', 'N/A')
        confidence_score = prediction.get('confidence_score', 0); confidence_pct = prediction.get('confidence_percentage', 0)
        result_color = colors.HexColor('#EF4444') if pred_class == 1 else colors.HexColor('#10B981')
        prediction_table = Table([['Classification:', pred_label], ['Class:', str(pred_class)], ['Confidence Score:', f'{confidence_score:.4f}'], ['Confidence Percentage:', f'{confidence_pct:.2f}%']], colWidths=[2*inch, 4*inch])
        prediction_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F3F4F6')), ('BACKGROUND', (1, 0), (1, 0), result_color), ('TEXTCOLOR', (0, 0), (-1, -1), colors.black), ('TEXTCOLOR', (1, 0), (1, 0), colors.white), ('ALIGN', (0, 0), (-1, -1), 'LEFT'), ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'), ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'), ('FONTSIZE', (0, 0), (-1, -1), 11), ('BOTTOMPADDING', (0, 0), (-1, -1), 10), ('TOPPADDING', (0, 0), (-1, -1), 10), ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)]))
        elements.append(prediction_table)
        elements.append(Spacer(1, 0.3 * inch))
        elements.append(Paragraph("Clinical Risk Assessment", heading_style))
        risk_assessment = prediction_data.get('risk_assessment', 'N/A'); recommendation = prediction_data.get('recommendation', 'N/A')
        if 'High Risk' in risk_assessment:
            risk_color, risk_border = colors.HexColor('#FEE2E2'), colors.HexColor('#EF4444')
        elif 'Moderate Risk' in risk_assessment:
            risk_color, risk_border = colors.HexColor('#FEF3C7'), colors.HexColor('#F59E0B')
        elif 'Borderline' in risk_assessment:
            risk_color, risk_border = colors.HexColor('#DBEAFE'), colors.HexColor('#3B82F6')
        else:
            risk_color, risk_border = colors.HexColor('#D1FAE5'), colors.HexColor('#10B981')
        risk_table = Table([['Risk Level:', risk_assessment], ['Clinical Recommendation:', recommendation]], colWidths=[2*inch, 4*inch])
        risk_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), risk_color), ('TEXTCOLOR', (0, 0), (-1, -1), colors.black), ('ALIGN', (0, 0), (-1, -1), 'LEFT'), ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'), ('FONTNAME', (1, 0), (1, -1), 'Helvetica'), ('FONTSIZE', (0, 0), (-1, -1), 11), ('BOTTOMPADDING', (0, 0), (-1, -1), 10), ('TOPPADDING', (0, 0), (-1, -1), 10), ('GRID', (0, 0), (-1, -1), 2, risk_border), ('VALIGN', (0, 0), (-1, -1), 'TOP')]))
        elements.append(risk_table)
        elements.append(Spacer(1, 0.3 * inch))
        if gradcam_data and gradcam_data.get('images'):
            elements.append(PageBreak())
            elements.append(Paragraph("Model Attention Visualization (Grad-CAM)", heading_style))
            elements.append(Paragraph("The following heatmap shows which regions of the image the AI model focused on when making its prediction. Red/yellow areas indicate regions of high importance, while blue areas are less relevant.", normal_style))
            elements.append(Spacer(1, 0.2 * inch))
            try:
                overlay_base64 = gradcam_data['images'].get('overlay', '')
                if overlay_base64:
                    overlay_buffer = BytesIO(base64.b64decode(overlay_base64))
                    elements.append(Image(overlay_buffer, width=4*inch, height=4*inch))
                    elements.append(Paragraph(f"<i>Grad-CAM Overlay - Layer: {gradcam_data.get('layer_used', 'N/A')}</i>", normal_style))
            except Exception as e:
                logger.warning(f"Grad-CAM image error: {str(e)}")
                elements.append(Paragraph("<i>Grad-CAM visualization could not be included in this report.</i>", normal_style))
        elements.append(Spacer(1, 0.4 * inch))
        elements.append(Paragraph("Medical Disclaimer", heading_style))
        disclaimer_text = "<b>IMPORTANT MEDICAL DISCLAIMER:</b><br/><br/>This report is generated by an AI-assisted tool for research and educational purposes only. This analysis should <b>NOT</b> be used as a substitute for professional medical diagnosis, treatment, or advice. The results provided are based on machine learning algorithms and may contain errors or uncertainties.<br/><br/><b>Always consult with qualified healthcare professionals</b> including radiologists, endocrinologists, or oncologists for:<br/>• Definitive diagnosis<br/>• Treatment planning and decisions<br/>• Medical advice and recommendations<br/><br/>This tool is <b>NOT FDA-approved</b> and is not intended for clinical decision-making. The developers and operators of this system assume no liability for any medical decisions made using this analysis."
        disclaimer_style = ParagraphStyle('Disclaimer', parent=styles['Normal'], fontSize=9, textColor=colors.HexColor('#666666'), spaceAfter=12, alignment=TA_JUSTIFY, leading=12)
        disclaimer_box = Table([[Paragraph(disclaimer_text, disclaimer_style)]], colWidths=[6.5*inch])
        disclaimer_box.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FEF3C7')), ('BORDER', (0, 0), (-1, -1), 2, colors.HexColor('#F59E0B')), ('PADDING', (0, 0), (-1, -1), 12)]))
        elements.append(disclaimer_box)
        elements.append(Spacer(1, 0.3 * inch))
        elements.append(Paragraph(f"<i>Report generated by Thyroid Cancer Detection System v2.0.0 on {timestamp}</i>", ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=colors.grey, alignment=TA_CENTER)))
        doc.build(elements); buffer.seek(0)
        logger.info("PDF report generated")
        return buffer
    except Exception as e:
        logger.error(f"PDF generation error: {str(e)}", exc_info=True)
        raise Exception(f"PDF generation failed: {str(e)}")
