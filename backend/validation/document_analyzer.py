"""
Document Analyzer
Extracts text and analyzes model validation documents (PDF, DOCX, CSV)
Detects SR 11-7 sections and extracts model information
"""

import os
import re
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import logging

# Document processing libraries
try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

try:
    from docx import Document
except ImportError:
    Document = None

import pandas as pd


class DocumentAnalyzer:
    """
    Analyze model validation documents and extract key information.
    
    Supports:
    - PDF text extraction
    - DOCX text extraction
    - CSV data loading
    - SR 11-7 section detection
    - Model information extraction
    """
    
    # SR 11-7 section keywords
    SR_11_7_SECTIONS = {
        "model_purpose": [
            "model purpose", "objective", "use case", "business purpose",
            "model description", "intended use"
        ],
        "conceptual_soundness": [
            "conceptual soundness", "theoretical foundation", "methodology",
            "model theory", "approach", "technique"
        ],
        "data_quality": [
            "data quality", "data source", "data validation", "data integrity",
            "sample size", "data representativeness", "data completeness"
        ],
        "performance": [
            "model performance", "accuracy", "discrimination", "calibration",
            "ks statistic", "gini", "auc", "roc", "confusion matrix"
        ],
        "stability": [
            "stability", "psi", "csi", "population stability", 
            "characteristic stability", "drift", "model monitoring"
        ],
        "assumptions": [
            "assumptions", "model assumptions", "key assumptions",
            "assumption testing", "sensitivity analysis"
        ],
        "implementation": [
            "implementation", "deployment", "production", "rollout",
            "model implementation", "system integration"
        ],
        "limitations": [
            "limitations", "model limitations", "constraints", "weaknesses",
            "known issues", "caveats"
        ],
        "recommendations": [
            "recommendations", "conclusion", "findings", "summary",
            "next steps", "action items"
        ]
    }
    
    # Model information patterns
    MODEL_INFO_PATTERNS = {
        "model_name": r"model\s+name[:\s]+([^\n]+)",
        "model_type": r"model\s+type[:\s]+([^\n]+)",
        "scorecard_type": r"scorecard\s+type[:\s]+([^\n]+)",
        "product_type": r"product\s+type[:\s]+([^\n]+)",
        "version": r"version[:\s]+([^\n]+)",
        "date": r"date[:\s]+([^\n]+)",
        "developer": r"developer[:\s]+([^\n]+)",
        "validator": r"validator[:\s]+([^\n]+)"
    }
    
    def __init__(self):
        """Initialize the document analyzer."""
        self.logger = logging.getLogger(__name__)
    
    def analyze_document(
        self, 
        file_path: str, 
        file_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze a document and extract all relevant information.
        
        Args:
            file_path: Path to the document file
            file_type: File type (pdf, docx, csv). Auto-detected if None.
            
        Returns:
            Dictionary with extracted information
        """
        try:
            # Detect file type if not provided
            if file_type is None:
                file_type = self._detect_file_type(file_path)
            
            # Extract text based on file type
            if file_type == "pdf":
                text = self._extract_pdf_text(file_path)
            elif file_type == "docx":
                text = self._extract_docx_text(file_path)
            elif file_type == "csv":
                return self._analyze_csv(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
            
            # Analyze the extracted text
            analysis = {
                "file_path": file_path,
                "file_type": file_type,
                "file_size": os.path.getsize(file_path),
                "analyzed_at": datetime.utcnow().isoformat(),
                "text_length": len(text),
                "model_info": self._extract_model_info(text),
                "sr_11_7_sections": self._detect_sr_11_7_sections(text),
                "key_metrics": self._extract_key_metrics(text),
                "summary": self._generate_summary(text)
            }
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing document: {e}")
            return {
                "error": str(e),
                "file_path": file_path,
                "analyzed_at": datetime.utcnow().isoformat()
            }
    
    def _detect_file_type(self, file_path: str) -> str:
        """Detect file type from extension."""
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            return "pdf"
        elif ext in [".docx", ".doc"]:
            return "docx"
        elif ext == ".csv":
            return "csv"
        else:
            raise ValueError(f"Unsupported file extension: {ext}")
    
    def _extract_pdf_text(self, file_path: str) -> str:
        """Extract text from PDF file."""
        if PdfReader is None:
            raise ImportError("pypdf is not installed. Install with: pip install pypdf")
        
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            self.logger.error(f"Error extracting PDF text: {e}")
            raise
    
    def _extract_docx_text(self, file_path: str) -> str:
        """Extract text from DOCX file."""
        if Document is None:
            raise ImportError("python-docx is not installed. Install with: pip install python-docx")
        
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            self.logger.error(f"Error extracting DOCX text: {e}")
            raise
    
    def _analyze_csv(self, file_path: str) -> Dict[str, Any]:
        """Analyze CSV file (data file)."""
        try:
            df = pd.read_csv(file_path)
            
            return {
                "file_path": file_path,
                "file_type": "csv",
                "file_size": os.path.getsize(file_path),
                "analyzed_at": datetime.utcnow().isoformat(),
                "data_info": {
                    "rows": len(df),
                    "columns": len(df.columns),
                    "column_names": df.columns.tolist(),
                    "dtypes": df.dtypes.astype(str).to_dict(),
                    "missing_values": df.isnull().sum().to_dict(),
                    "sample_data": df.head(5).to_dict()
                }
            }
        except Exception as e:
            self.logger.error(f"Error analyzing CSV: {e}")
            return {
                "error": str(e),
                "file_path": file_path,
                "analyzed_at": datetime.utcnow().isoformat()
            }
    
    def _extract_model_info(self, text: str) -> Dict[str, Any]:
        """Extract model information from text."""
        model_info = {}
        text_lower = text.lower()
        
        for key, pattern in self.MODEL_INFO_PATTERNS.items():
            match = re.search(pattern, text_lower, re.IGNORECASE)
            if match:
                model_info[key] = match.group(1).strip()
        
        # Extract additional info
        model_info["has_model_card"] = "model card" in text_lower
        model_info["has_validation_report"] = "validation report" in text_lower
        model_info["has_performance_metrics"] = any(
            metric in text_lower 
            for metric in ["accuracy", "precision", "recall", "auc", "gini", "ks"]
        )
        
        return model_info
    
    def _detect_sr_11_7_sections(self, text: str) -> Dict[str, Any]:
        """Detect SR 11-7 sections in the document."""
        text_lower = text.lower()
        sections_found = {}
        
        for section_name, keywords in self.SR_11_7_SECTIONS.items():
            # Check if any keyword is present
            found = any(keyword in text_lower for keyword in keywords)
            
            if found:
                # Find the section content
                section_content = self._extract_section_content(text, keywords)
                sections_found[section_name] = {
                    "present": True,
                    "keywords_found": [kw for kw in keywords if kw in text_lower],
                    "content_length": len(section_content),
                    "preview": section_content[:200] if section_content else ""
                }
            else:
                sections_found[section_name] = {
                    "present": False,
                    "keywords_found": [],
                    "content_length": 0,
                    "preview": ""
                }
        
        # Calculate coverage
        total_sections = len(self.SR_11_7_SECTIONS)
        sections_present = sum(1 for s in sections_found.values() if s["present"])
        coverage_percentage = (sections_present / total_sections) * 100
        
        return {
            "sections": sections_found,
            "coverage": {
                "sections_present": sections_present,
                "total_sections": total_sections,
                "percentage": round(coverage_percentage, 1)
            }
        }
    
    def _extract_section_content(self, text: str, keywords: List[str]) -> str:
        """Extract content for a specific section."""
        text_lower = text.lower()
        
        # Find the first occurrence of any keyword
        positions = []
        for keyword in keywords:
            pos = text_lower.find(keyword)
            if pos != -1:
                positions.append(pos)
        
        if not positions:
            return ""
        
        # Get content starting from the first keyword
        start_pos = min(positions)
        # Extract up to 1000 characters or next section
        end_pos = min(start_pos + 1000, len(text))
        return text[start_pos:end_pos]
    
    def _extract_key_metrics(self, text: str) -> Dict[str, Any]:
        """Extract key performance metrics from text."""
        metrics = {}
        text_lower = text.lower()
        
        # Common metric patterns
        metric_patterns = {
            "gini": r"gini[:\s]+([0-9.]+)",
            "ks": r"ks[:\s]+([0-9.]+)",
            "auc": r"auc[:\s]+([0-9.]+)",
            "accuracy": r"accuracy[:\s]+([0-9.]+)",
            "precision": r"precision[:\s]+([0-9.]+)",
            "recall": r"recall[:\s]+([0-9.]+)",
            "psi": r"psi[:\s]+([0-9.]+)",
            "csi": r"csi[:\s]+([0-9.]+)"
        }
        
        for metric_name, pattern in metric_patterns.items():
            match = re.search(pattern, text_lower)
            if match:
                try:
                    metrics[metric_name] = float(match.group(1))
                except ValueError:
                    pass
        
        return metrics
    
    def _generate_summary(self, text: str) -> Dict[str, Any]:
        """Generate a summary of the document."""
        text_lower = text.lower()
        
        # Count key terms
        key_terms = {
            "model": text_lower.count("model"),
            "validation": text_lower.count("validation"),
            "performance": text_lower.count("performance"),
            "risk": text_lower.count("risk"),
            "data": text_lower.count("data"),
            "scorecard": text_lower.count("scorecard")
        }
        
        # Detect document type
        doc_type = "unknown"
        if "validation report" in text_lower:
            doc_type = "validation_report"
        elif "model card" in text_lower:
            doc_type = "model_card"
        elif "model documentation" in text_lower:
            doc_type = "model_documentation"
        elif "technical specification" in text_lower:
            doc_type = "technical_specification"
        
        return {
            "document_type": doc_type,
            "key_term_counts": key_terms,
            "estimated_pages": len(text) // 3000,  # Rough estimate
            "has_tables": "table" in text_lower,
            "has_charts": any(word in text_lower for word in ["chart", "graph", "figure"]),
            "has_code": any(word in text_lower for word in ["code", "script", "function"])
        }
    
    def validate_file(
        self,
        filename: str,
        file_size: int = None,
        allowed_types: List[str] = None,
        max_size_mb: int = 50
    ) -> Dict[str, Any]:
        """
        Validate if a file is acceptable for processing.
        
        Args:
            filename: Name of the file (with extension)
            file_size: Size of file in bytes (optional, for pre-upload validation)
            allowed_types: List of allowed file types
            max_size_mb: Maximum file size in MB
            
        Returns:
            Dictionary with validation result
        """
        if allowed_types is None:
            allowed_types = ["pdf", "docx", "csv"]
        
        # Extract file extension
        ext = os.path.splitext(filename)[1].lower().lstrip('.')
        
        # Check file type
        if ext not in allowed_types:
            return {
                "valid": False,
                "error": f"File type '.{ext}' not supported. Allowed types: {', '.join(allowed_types)}",
                "file_type": ext
            }
        
        # Check file size if provided
        if file_size is not None:
            file_size_mb = file_size / (1024 * 1024)
            if file_size_mb > max_size_mb:
                return {
                    "valid": False,
                    "error": f"File size ({file_size_mb:.1f}MB) exceeds maximum ({max_size_mb}MB)",
                    "file_type": ext
                }
        
        return {
            "valid": True,
            "file_type": ext,
            "message": "File is valid"
        }
    
    def extract_metadata(self, file_path: str) -> Dict[str, Any]:
        """Extract file metadata with error handling."""
        try:
            if not os.path.exists(file_path):
                return {
                    "filename": os.path.basename(file_path),
                    "file_path": file_path,
                    "file_extension": os.path.splitext(file_path)[1].lower().lstrip('.'),
                    "error": "File does not exist"
                }
            
            stat = os.stat(file_path)
            
            return {
                "filename": os.path.basename(file_path),
                "file_path": file_path,
                "file_extension": os.path.splitext(file_path)[1].lower().lstrip('.'),
                "file_type": self._detect_file_type(file_path),
                "size_bytes": stat.st_size,
                "size_mb": round(stat.st_size / (1024 * 1024), 2),
                "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat()
            }
        except Exception as e:
            return {
                "filename": os.path.basename(file_path),
                "file_path": file_path,
                "file_extension": os.path.splitext(file_path)[1].lower().lstrip('.'),
                "error": str(e)
            }


# Made with Bob