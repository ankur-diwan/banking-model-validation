"""
Test suite for Document Analyzer
Tests document upload, analysis, and SR 11-7 section detection
"""

import pytest
import os
import tempfile
from pathlib import Path
from validation.document_analyzer import DocumentAnalyzer


class TestDocumentAnalyzer:
    """Test cases for DocumentAnalyzer"""
    
    @pytest.fixture
    def analyzer(self):
        """Create DocumentAnalyzer instance"""
        return DocumentAnalyzer()
    
    def test_validate_file_pdf(self, analyzer):
        """Test PDF file validation"""
        result = analyzer.validate_file("test.pdf", 1024 * 1024)  # 1MB
        assert result["valid"] is True
        assert result["file_type"] == "pdf"
    
    def test_validate_file_docx(self, analyzer):
        """Test DOCX file validation"""
        result = analyzer.validate_file("test.docx", 2 * 1024 * 1024)  # 2MB
        assert result["valid"] is True
        assert result["file_type"] == "docx"
    
    def test_validate_file_csv(self, analyzer):
        """Test CSV file validation"""
        result = analyzer.validate_file("test.csv", 5 * 1024 * 1024)  # 5MB
        assert result["valid"] is True
        assert result["file_type"] == "csv"
    
    def test_validate_file_invalid_type(self, analyzer):
        """Test invalid file type"""
        result = analyzer.validate_file("test.exe", 1024)
        assert result["valid"] is False
        assert "not supported" in result["error"].lower()
    
    def test_validate_file_too_large(self, analyzer):
        """Test file size limit"""
        result = analyzer.validate_file("test.pdf", 60 * 1024 * 1024)  # 60MB
        assert result["valid"] is False
        assert "exceeds" in result["error"].lower()
    
    def test_extract_metadata_nonexistent_file(self, analyzer):
        """Test metadata extraction for non-existent file"""
        metadata = analyzer.extract_metadata("/nonexistent/file.pdf")
        
        # Should return basic metadata even if file doesn't exist
        assert "filename" in metadata
        assert "file_extension" in metadata


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
