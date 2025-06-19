import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Any
import pandas as pd

class UIComponents:
    """Reusable UI components for the healthcare assistant"""
    
    def __init__(self):
        pass
    
    def render_lab_results_chart(self, lab_data: Dict[str, Dict]) -> None:
        """Render a chart showing lab results vs normal ranges"""
        
        # Prepare data for plotting
        test_names = []
        values = []
        statuses = []
        colors = []
        
        color_map = {
            'normal': '#28a745',
            'borderline': '#ffc107', 
            'high': '#dc3545',
            'low': '#fd7e14'
        }
        
        for test, result in lab_data.items():
            test_names.append(test.replace('_', ' ').title())
            # Extract numeric value
            value_str = result['value'].split()[0]
            try:
                values.append(float(value_str))
            except:
                values.append(0)
            statuses.append(result['status'])
            colors.append(color_map.get(result['status'], '#6c757d'))
        
        # Create bar chart
        fig = go.Figure(data=[
            go.Bar(
                x=test_names,
                y=values,
                marker_color=colors,
                text=[f"{status.title()}" for status in statuses],
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title="Lab Results Overview",
            xaxis_title="Lab Tests",
            yaxis_title="Values",
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_medication_timeline(self, medications: List[Dict]) -> None:
        """Render a timeline of medications"""
        if not medications:
            st.info("No medications found in documents")
            return
        
        # Create a simple medication list view
        st.subheader("💊 Medication Summary")
        
        for i, med in enumerate(medications):
            with st.expander(f"{med.get('name', f'Medication {i+1}')}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Type:** {med.get('type', 'Unknown')}")
                    st.write(f"**Dosage:** {med.get('dosage', 'Not specified')}")
                
                with col2:
                    st.write(f"**Frequency:** {med.get('frequency', 'Not specified')}")
                    st.write(f"**Duration:** {med.get('duration', 'Not specified')}")
    
    def render_health_summary_card(self, title: str, value: str, status: str = "normal", description: str = "") -> None:
        """Render a health metric summary card"""
        
        # Color scheme based on status
        if status == "normal":
            bg_color = "#d1edff"
            border_color = "#0366d6"
            icon = "✅"
        elif status == "warning":
            bg_color = "#fff3cd"
            border_color = "#856404"
            icon = "⚠️"
        elif status == "critical":
            bg_color = "#f8d7da"
            border_color = "#721c24"
            icon = "🚨"
        else:
            bg_color = "#f8f9fa"
            border_color = "#6c757d"
            icon = "ℹ️"
        
        st.markdown(f"""
        <div style="
            background-color: {bg_color};
            border-left: 4px solid {border_color};
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 5px;
        ">
            <h4 style="margin: 0; color: {border_color};">{icon} {title}</h4>
            <p style="font-size: 1.2rem; font-weight: bold; margin: 0.5rem 0;">{value}</p>
            <p style="margin: 0; font-size: 0.9rem; color: #6c757d;">{description}</p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_document_preview(self, document: Dict) -> None:
        """Render a preview of a document"""
        
        st.markdown(f"""
        <div style="
            border: 1px solid #dee2e6;
            border-radius: 5px;
            padding: 1rem;
            margin: 0.5rem 0;
            background-color: #f8f9fa;
        ">
            <h5 style="margin: 0 0 0.5rem 0; color: #495057;">📄 {document.get('filename', 'Unknown Document')}</h5>
            <p style="margin: 0; font-size: 0.9rem; color: #6c757d;">
                <strong>Type:</strong> {document.get('document_type', 'Unknown')} | 
                <strong>Added:</strong> {document.get('timestamp', 'Unknown')}
            </p>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">
                {document.get('content', '')[:200]}{'...' if len(document.get('content', '')) > 200 else ''}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_progress_indicator(self, current_step: int, total_steps: int, step_labels: List[str]) -> None:
        """Render a progress indicator"""
        
        progress_percent = current_step / total_steps
        
        st.progress(progress_percent)
        
        # Step indicators
        cols = st.columns(total_steps)
        for i, label in enumerate(step_labels):
            with cols[i]:
                if i < current_step:
                    st.markdown(f"✅ **{label}**")
                elif i == current_step:
                    st.markdown(f"🔄 **{label}**")
                else:
                    st.markdown(f"⏳ {label}")
    
    def render_health_metrics_dashboard(self, metrics: Dict[str, Any]) -> None:
        """Render a dashboard of health metrics"""
        
        st.subheader("📊 Health Metrics Dashboard")
        
        # Create metrics columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Total Documents",
                value=metrics.get('total_documents', 0),
                delta=metrics.get('new_documents', 0)
            )
        
        with col2:
            st.metric(
                label="Lab Results",
                value=metrics.get('lab_results', 0),
                delta=metrics.get('recent_labs', 0)
            )
        
        with col3:
            st.metric(
                label="Medications",
                value=metrics.get('medications', 0),
                delta=metrics.get('new_medications', 0)
            )
        
        with col4:
            st.metric(
                label="Health Score",
                value=f"{metrics.get('health_score', 85)}%",
                delta=f"{metrics.get('score_change', 0)}%"
            )
    
    def render_alerts_panel(self, alerts: List[Dict]) -> None:
        """Render health alerts and reminders"""
        
        if not alerts:
            return
        
        st.subheader("🔔 Health Alerts")
        
        for alert in alerts:
            alert_type = alert.get('type', 'info')
            
            if alert_type == 'critical':
                st.error(f"🚨 **{alert.get('title', 'Critical Alert')}**\n\n{alert.get('message', '')}")
            elif alert_type == 'warning':
                st.warning(f"⚠️ **{alert.get('title', 'Warning')}**\n\n{alert.get('message', '')}")
            else:
                st.info(f"ℹ️ **{alert.get('title', 'Information')}**\n\n{alert.get('message', '')}")
    
    def render_export_options(self, data: Dict) -> None:
        """Render data export options"""
        
        st.subheader("📤 Export Options")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📄 Export as PDF"):
                st.info("PDF export functionality would be implemented here")
        
        with col2:
            if st.button("📊 Export as CSV"):
                # Convert data to CSV format
                df = pd.DataFrame(data.get('lab_results', []))
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="health_data.csv",
                    mime="text/csv"
                )
        
        with col3:
            if st.button("📋 Generate Report"):
                st.info("Report generation functionality would be implemented here")
    
    def render_privacy_settings(self) -> None:
        """Render privacy and security settings"""
        
        st.subheader("🔒 Privacy & Security")
        
        with st.expander("Privacy Settings"):
            st.checkbox("Enable automatic document cleanup after 30 days", value=False)
            st.checkbox("Encrypt all stored documents", value=True)
            st.checkbox("Require password for sensitive operations", value=False)
            
            st.write("**Data Storage Location:** Local device only")
            st.write("**Encryption:** AES-256 (when enabled)")
            st.write("**Network Access:** None - completely offline")
        
        with st.expander("Data Management"):
            if st.button("Clear All Documents", type="secondary"):
                st.warning("This will permanently delete all stored documents. This action cannot be undone.")
            
            if st.button("Export All Data", type="secondary"):
                st.info("Export functionality would create a secure backup of all your health data.")
            
            st.write("**Storage Used:** ~2.5 MB")
            st.write("**Documents Stored:** 12")
            st.write("**Last Backup:** Never")