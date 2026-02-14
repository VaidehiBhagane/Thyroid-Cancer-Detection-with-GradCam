"""
PDF Report Generation for Thyroid Cancer Detection
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from io import BytesIO
import base64
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def generate_pdf_report(prediction_data: dict, gradcam_data: dict = None) -> BytesIO:
    """
    Generate a comprehensive PDF report for thyroid cancer detection analysis.
    
    Args:
        prediction_data: Dictionary containing prediction results
        gradcam_data: Optional dictionary containing Grad-CAM visualization data
    
    Returns:
        BytesIO: PDF file as bytes
    """
    try:
        # Create PDF in memory
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        # Container for PDF elements
        elements = []
        
        # Define styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#0066CC'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#333333'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=12,
            alignment=TA_LEFT
        )
        
        # Title
        title = Paragraph("🦋 Thyroid Cancer Detection Report", title_style)
        elements.append(title)
        elements.append(Spacer(1, 0.2 * inch))
        
        # Report metadata
        timestamp = prediction_data.get('timestamp', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        filename = prediction_data.get('filename', 'Unknown')
        
        metadata_data = [
            ['Report Generated:', timestamp],
            ['Image Filename:', filename],
            ['Report Type:', 'AI-Assisted Analysis']
        ]
        
        metadata_table = Table(metadata_data, colWidths=[2*inch, 4*inch])
        metadata_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F3F4F6')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        
        elements.append(metadata_table)
        elements.append(Spacer(1, 0.3 * inch))
        
        # Prediction Results Section
        elements.append(Paragraph("Prediction Results", heading_style))
        
        prediction = prediction_data.get('prediction', {})
        pred_class = prediction.get('class', 'N/A')
        pred_label = prediction.get('label', 'N/A')
        confidence_score = prediction.get('confidence_score', 0)
        confidence_pct = prediction.get('confidence_percentage', 0)
        
        # Determine color based on classification
        if pred_class == 1:
            result_color = colors.HexColor('#EF4444')  # Red for malignant
        else:
            result_color = colors.HexColor('#10B981')  # Green for benign
        
        prediction_data_table = [
            ['Classification:', pred_label],
            ['Class:', str(pred_class)],
            ['Confidence Score:', f'{confidence_score:.4f}'],
            ['Confidence Percentage:', f'{confidence_pct:.2f}%']
        ]
        
        prediction_table = Table(prediction_data_table, colWidths=[2*inch, 4*inch])
        prediction_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F3F4F6')),
            ('BACKGROUND', (1, 0), (1, 0), result_color),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('TEXTCOLOR', (1, 0), (1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        
        elements.append(prediction_table)
        elements.append(Spacer(1, 0.3 * inch))
        
        # Clinical Assessment Section
        elements.append(Paragraph("Clinical Risk Assessment", heading_style))
        
        risk_assessment = prediction_data.get('risk_assessment', 'N/A')
        recommendation = prediction_data.get('recommendation', 'N/A')
        
        # Risk assessment box
        if 'High Risk' in risk_assessment:
            risk_color = colors.HexColor('#FEE2E2')
            risk_border = colors.HexColor('#EF4444')
        elif 'Moderate Risk' in risk_assessment:
            risk_color = colors.HexColor('#FEF3C7')
            risk_border = colors.HexColor('#F59E0B')
        elif 'Borderline' in risk_assessment:
            risk_color = colors.HexColor('#DBEAFE')
            risk_border = colors.HexColor('#3B82F6')
        else:
            risk_color = colors.HexColor('#D1FAE5')
            risk_border = colors.HexColor('#10B981')
        
        risk_data = [
            ['Risk Level:', risk_assessment],
            ['Clinical Recommendation:', recommendation]
        ]
        
        risk_table = Table(risk_data, colWidths=[2*inch, 4*inch])
        risk_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), risk_color),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 2, risk_border),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))
        
        elements.append(risk_table)
        elements.append(Spacer(1, 0.3 * inch))
        
        # Grad-CAM Visualization (if available)
        if gradcam_data and gradcam_data.get('images'):
            elements.append(PageBreak())
            elements.append(Paragraph("Model Attention Visualization (Grad-CAM)", heading_style))
            
            description = Paragraph(
                "The following heatmap shows which regions of the image the AI model focused on when making its prediction. "
                "Red/yellow areas indicate regions of high importance, while blue areas are less relevant.",
                normal_style
            )
            elements.append(description)
            elements.append(Spacer(1, 0.2 * inch))
            
            try:
                # Decode and add overlay image
                overlay_base64 = gradcam_data['images'].get('overlay', '')
                if overlay_base64:
                    overlay_bytes = base64.b64decode(overlay_base64)
                    overlay_buffer = BytesIO(overlay_bytes)
                    
                    # Add image with caption
                    img = Image(overlay_buffer, width=4*inch, height=4*inch)
                    elements.append(img)
                    
                    caption = Paragraph(
                        f"<i>Grad-CAM Overlay - Layer: {gradcam_data.get('layer_used', 'N/A')}</i>",
                        normal_style
                    )
                    elements.append(caption)
            except Exception as e:
                logger.warning(f"Could not add Grad-CAM image to PDF: {str(e)}")
                error_text = Paragraph(
                    "<i>Grad-CAM visualization could not be included in this report.</i>",
                    normal_style
                )
                elements.append(error_text)
        
        # Medical Disclaimer
        elements.append(Spacer(1, 0.4 * inch))
        elements.append(Paragraph("Medical Disclaimer", heading_style))
        
        disclaimer_text = """
        <b>IMPORTANT MEDICAL DISCLAIMER:</b><br/><br/>
        This report is generated by an AI-assisted tool for research and educational purposes only. 
        This analysis should <b>NOT</b> be used as a substitute for professional medical diagnosis, treatment, 
        or advice. The results provided are based on machine learning algorithms and may contain errors or 
        uncertainties.<br/><br/>
        <b>Always consult with qualified healthcare professionals</b> including radiologists, endocrinologists, 
        or oncologists for:<br/>
        • Definitive diagnosis<br/>
        • Treatment planning and decisions<br/>
        • Medical advice and recommendations<br/><br/>
        This tool is <b>NOT FDA-approved</b> and is not intended for clinical decision-making. 
        The developers and operators of this system assume no liability for any medical decisions made 
        using this analysis.
        """
        
        disclaimer_style = ParagraphStyle(
            'Disclaimer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#666666'),
            spaceAfter=12,
            alignment=TA_JUSTIFY,
            leading=12
        )
        
        disclaimer = Paragraph(disclaimer_text, disclaimer_style)
        
        disclaimer_box = Table([[disclaimer]], colWidths=[6.5*inch])
        disclaimer_box.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FEF3C7')),
            ('BORDER', (0, 0), (-1, -1), 2, colors.HexColor('#F59E0B')),
            ('PADDING', (0, 0), (-1, -1), 12)
        ]))
        
        elements.append(disclaimer_box)
        
        # Footer
        elements.append(Spacer(1, 0.3 * inch))
        footer_text = Paragraph(
            f"<i>Report generated by Thyroid Cancer Detection System v2.0.0 on {timestamp}</i>",
            ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=colors.grey, alignment=TA_CENTER)
        )
        elements.append(footer_text)
        
        # Build PDF
        doc.build(elements)
        
        # Get PDF bytes
        buffer.seek(0)
        logger.info("PDF report generated successfully")
        return buffer
        
    except Exception as e:
        logger.error(f"Error generating PDF report: {str(e)}", exc_info=True)
        raise Exception(f"Failed to generate PDF report: {str(e)}")
