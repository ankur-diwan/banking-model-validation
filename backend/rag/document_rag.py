"""
RAG (Retrieval Augmented Generation) System for Document Understanding
Processes development documentation including text, equations, tables, diagrams, graphs, and code
"""

import os
from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime
from loguru import logger
import json
import re


class DocumentChunk:
    """Represents a chunk of document content"""
    
    def __init__(
        self,
        chunk_id: str,
        content: str,
        content_type: str,
        metadata: Dict[str, Any],
        embedding: Optional[List[float]] = None
    ):
        self.chunk_id = chunk_id
        self.content = content
        self.content_type = content_type  # text, equation, table, diagram, graph, code
        self.metadata = metadata
        self.embedding = embedding
        self.created_at = datetime.utcnow()
    
    def to_dict(self) -> Dict:
        return {
            "chunk_id": self.chunk_id,
            "content": self.content,
            "content_type": self.content_type,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
        }


class DocumentRAG:
    """
    RAG system for understanding model development documentation
    Uses watsonx.ai for embeddings and generation
    """
    
    def __init__(self, watsonx_client):
        """
        Initialize RAG system
        
        Args:
            watsonx_client: watsonx.ai client for embeddings and generation
        """
        self.watsonx = watsonx_client
        self.documents = {}
        self.chunks = {}
        self.chunk_index = {}  # Simple in-memory index (use vector DB in production)
        
        # Evaluation metrics
        self.metrics = {
            "retrieval_precision": [],
            "retrieval_recall": [],
            "answer_relevance": [],
            "faithfulness": [],
            "context_relevance": [],
        }
        
        logger.info("Document RAG system initialized")
    
    # ==================== Document Processing ====================
    
    async def ingest_document(
        self,
        document_id: str,
        document_path: str,
        document_type: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Ingest a development document
        
        Args:
            document_id: Unique document identifier
            document_path: Path to document file
            document_type: Type of document (pdf, docx, md, etc.)
            metadata: Additional metadata
            
        Returns:
            Ingestion results
        """
        logger.info(f"Ingesting document: {document_id}")
        
        try:
            # Extract content based on document type
            if document_type == "pdf":
                content = await self._extract_pdf_content(document_path)
            elif document_type == "docx":
                content = await self._extract_docx_content(document_path)
            elif document_type == "md":
                content = await self._extract_markdown_content(document_path)
            else:
                content = await self._extract_text_content(document_path)
            
            # Parse different content types
            chunks = await self._parse_content(content, document_id)
            
            # Generate embeddings for chunks
            for chunk in chunks:
                embedding = await self._generate_embedding(chunk.content)
                chunk.embedding = embedding
                self.chunks[chunk.chunk_id] = chunk
                
                # Add to index
                if chunk.content_type not in self.chunk_index:
                    self.chunk_index[chunk.content_type] = []
                self.chunk_index[chunk.content_type].append(chunk)
            
            # Store document metadata
            self.documents[document_id] = {
                "document_id": document_id,
                "document_path": document_path,
                "document_type": document_type,
                "metadata": metadata or {},
                "chunk_count": len(chunks),
                "ingested_at": datetime.utcnow().isoformat(),
            }
            
            logger.info(f"Successfully ingested document {document_id} with {len(chunks)} chunks")
            
            return {
                "document_id": document_id,
                "chunks_created": len(chunks),
                "content_types": list(set(c.content_type for c in chunks)),
                "status": "success",
            }
            
        except Exception as e:
            logger.error(f"Failed to ingest document {document_id}: {e}")
            return {
                "document_id": document_id,
                "status": "failed",
                "error": str(e),
            }
    
    async def _extract_pdf_content(self, path: str) -> str:
        """Extract content from PDF (placeholder)"""
        # In production, use PyPDF2, pdfplumber, or similar
        return f"PDF content from {path}"
    
    async def _extract_docx_content(self, path: str) -> str:
        """Extract content from DOCX (placeholder)"""
        # In production, use python-docx
        return f"DOCX content from {path}"
    
    async def _extract_markdown_content(self, path: str) -> str:
        """Extract content from Markdown"""
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    
    async def _extract_text_content(self, path: str) -> str:
        """Extract content from text file"""
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    
    async def _parse_content(
        self,
        content: str,
        document_id: str
    ) -> List[DocumentChunk]:
        """
        Parse content into chunks by type
        
        Identifies:
        - Text paragraphs
        - Mathematical equations (LaTeX, MathML)
        - Tables (markdown, HTML)
        - Code blocks
        - Diagrams/graphs (references)
        """
        chunks = []
        chunk_counter = 0
        
        # Split content into sections
        sections = content.split('\n\n')
        
        for section in sections:
            if not section.strip():
                continue
            
            chunk_id = f"{document_id}_chunk_{chunk_counter}"
            chunk_counter += 1
            
            # Detect content type
            content_type = self._detect_content_type(section)
            
            # Create chunk
            chunk = DocumentChunk(
                chunk_id=chunk_id,
                content=section.strip(),
                content_type=content_type,
                metadata={
                    "document_id": document_id,
                    "position": chunk_counter,
                }
            )
            
            chunks.append(chunk)
        
        return chunks
    
    def _detect_content_type(self, content: str) -> str:
        """Detect the type of content"""
        # Check for code blocks
        if content.startswith('```') or content.startswith('    '):
            return "code"
        
        # Check for equations (LaTeX)
        if '$$' in content or '\\[' in content or '\\begin{equation}' in content:
            return "equation"
        
        # Check for tables (markdown)
        if '|' in content and content.count('|') > 2:
            return "table"
        
        # Check for diagram references
        if any(keyword in content.lower() for keyword in ['figure', 'diagram', 'chart', 'graph', 'plot']):
            return "diagram"
        
        # Default to text
        return "text"
    
    async def _generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text using watsonx.ai
        
        In production, use watsonx.ai embedding models
        For now, return a placeholder
        """
        # Placeholder: In production, call watsonx.ai embedding API
        # embedding = await self.watsonx.generate_embedding(text)
        
        # Return dummy embedding for demonstration
        import hashlib
        hash_val = int(hashlib.md5(text.encode()).hexdigest(), 16)
        return [(hash_val % 1000) / 1000.0] * 768  # 768-dim embedding
    
    # ==================== Retrieval ====================
    
    async def retrieve_relevant_chunks(
        self,
        query: str,
        top_k: int = 5,
        content_types: Optional[List[str]] = None
    ) -> List[DocumentChunk]:
        """
        Retrieve relevant chunks for a query
        
        Args:
            query: Search query
            top_k: Number of chunks to retrieve
            content_types: Filter by content types
            
        Returns:
            List of relevant chunks
        """
        logger.info(f"Retrieving chunks for query: {query[:50]}...")
        
        # Generate query embedding
        query_embedding = await self._generate_embedding(query)
        
        # Get candidate chunks
        candidates = []
        if content_types:
            for ct in content_types:
                candidates.extend(self.chunk_index.get(ct, []))
        else:
            candidates = list(self.chunks.values())
        
        # Calculate similarity scores
        scored_chunks = []
        for chunk in candidates:
            if chunk.embedding:
                similarity = self._cosine_similarity(query_embedding, chunk.embedding)
                scored_chunks.append((chunk, similarity))
        
        # Sort by similarity and return top-k
        scored_chunks.sort(key=lambda x: x[1], reverse=True)
        top_chunks = [chunk for chunk, score in scored_chunks[:top_k]]
        
        logger.info(f"Retrieved {len(top_chunks)} relevant chunks")
        return top_chunks
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        if len(vec1) != len(vec2):
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = sum(a * a for a in vec1) ** 0.5
        magnitude2 = sum(b * b for b in vec2) ** 0.5
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)
    
    # ==================== Generation ====================
    
    async def generate_answer(
        self,
        question: str,
        context_chunks: List[DocumentChunk],
        model_name: str = "ibm/granite-13b-chat-v2"
    ) -> Dict[str, Any]:
        """
        Generate answer using RAG
        
        Args:
            question: User question
            context_chunks: Retrieved context chunks
            model_name: watsonx.ai model to use
            
        Returns:
            Generated answer with metadata
        """
        logger.info(f"Generating answer for: {question[:50]}...")
        
        # Prepare context
        context = self._prepare_context(context_chunks)
        
        # Create prompt
        prompt = self._create_rag_prompt(question, context)
        
        # Generate answer using watsonx.ai
        # In production, call watsonx.ai generation API
        # answer = await self.watsonx.generate(prompt, model_name)
        
        # Placeholder answer
        answer = f"Based on the provided documentation, {question.lower()} can be addressed by considering the following aspects from the context..."
        
        return {
            "question": question,
            "answer": answer,
            "context_chunks": [c.chunk_id for c in context_chunks],
            "model_used": model_name,
            "generated_at": datetime.utcnow().isoformat(),
        }
    
    def _prepare_context(self, chunks: List[DocumentChunk]) -> str:
        """Prepare context from chunks"""
        context_parts = []
        
        for i, chunk in enumerate(chunks, 1):
            context_parts.append(f"[Context {i} - {chunk.content_type}]")
            context_parts.append(chunk.content)
            context_parts.append("")
        
        return "\n".join(context_parts)
    
    def _create_rag_prompt(self, question: str, context: str) -> str:
        """Create RAG prompt"""
        return f"""You are an expert model validator reviewing banking model documentation.

Context from documentation:
{context}

Question: {question}

Please provide a detailed answer based on the context above. If the context doesn't contain enough information, acknowledge this and provide general guidance based on SR 11-7 requirements.

Answer:"""
    
    # ==================== Validation Enhancement ====================
    
    async def enhance_validation(
        self,
        model_id: str,
        validation_type: str
    ) -> Dict[str, Any]:
        """
        Enhance validation using RAG
        
        Args:
            model_id: Model being validated
            validation_type: Type of validation
            
        Returns:
            Enhanced validation recommendations
        """
        logger.info(f"Enhancing validation for model {model_id}")
        
        # Retrieve relevant documentation
        query = f"validation requirements for {validation_type} model"
        relevant_chunks = await self.retrieve_relevant_chunks(query, top_k=10)
        
        # Generate validation recommendations
        recommendations = []
        
        # Check for model assumptions
        assumption_chunks = await self.retrieve_relevant_chunks(
            "model assumptions and limitations",
            top_k=5,
            content_types=["text", "equation"]
        )
        
        if assumption_chunks:
            recommendations.append({
                "category": "assumptions",
                "recommendation": "Review documented model assumptions",
                "references": [c.chunk_id for c in assumption_chunks],
            })
        
        # Check for data requirements
        data_chunks = await self.retrieve_relevant_chunks(
            "data requirements and quality",
            top_k=5,
            content_types=["text", "table"]
        )
        
        if data_chunks:
            recommendations.append({
                "category": "data_quality",
                "recommendation": "Validate data quality requirements",
                "references": [c.chunk_id for c in data_chunks],
            })
        
        # Check for performance metrics
        metric_chunks = await self.retrieve_relevant_chunks(
            "performance metrics and thresholds",
            top_k=5,
            content_types=["text", "equation", "table"]
        )
        
        if metric_chunks:
            recommendations.append({
                "category": "performance",
                "recommendation": "Verify performance metrics meet requirements",
                "references": [c.chunk_id for c in metric_chunks],
            })
        
        return {
            "model_id": model_id,
            "validation_type": validation_type,
            "recommendations": recommendations,
            "total_references": len(relevant_chunks),
        }
    
    async def generate_validation_documentation(
        self,
        model_id: str,
        validation_results: Dict[str, Any]
    ) -> str:
        """
        Generate validation documentation using RAG
        
        Args:
            model_id: Model ID
            validation_results: Validation test results
            
        Returns:
            Generated documentation text
        """
        logger.info(f"Generating validation documentation for {model_id}")
        
        # Retrieve relevant documentation templates
        template_chunks = await self.retrieve_relevant_chunks(
            "validation documentation template SR 11-7",
            top_k=10
        )
        
        # Generate documentation sections
        sections = []
        
        # Executive Summary
        sections.append("# Executive Summary\n")
        sections.append(f"This document presents the independent validation of model {model_id}.")
        sections.append("")
        
        # Model Purpose
        sections.append("# Model Purpose and Design\n")
        purpose_chunks = await self.retrieve_relevant_chunks(
            f"model {model_id} purpose and design",
            top_k=3
        )
        for chunk in purpose_chunks:
            sections.append(chunk.content)
        sections.append("")
        
        # Validation Results
        sections.append("# Validation Results\n")
        sections.append(f"Overall Status: {validation_results.get('status', 'Unknown')}")
        sections.append("")
        
        # Findings and Recommendations
        sections.append("# Findings and Recommendations\n")
        sections.append("Based on the validation testing, the following findings were identified:")
        sections.append("")
        
        return "\n".join(sections)
    
    # ==================== Evaluation Metrics ====================
    
    async def evaluate_retrieval(
        self,
        query: str,
        retrieved_chunks: List[DocumentChunk],
        relevant_chunk_ids: List[str]
    ) -> Dict[str, float]:
        """
        Evaluate retrieval quality
        
        Args:
            query: Search query
            retrieved_chunks: Retrieved chunks
            relevant_chunk_ids: Ground truth relevant chunk IDs
            
        Returns:
            Evaluation metrics
        """
        retrieved_ids = [c.chunk_id for c in retrieved_chunks]
        
        # Calculate precision
        true_positives = len(set(retrieved_ids) & set(relevant_chunk_ids))
        precision = true_positives / len(retrieved_ids) if retrieved_ids else 0.0
        
        # Calculate recall
        recall = true_positives / len(relevant_chunk_ids) if relevant_chunk_ids else 0.0
        
        # Calculate F1 score
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        
        metrics = {
            "precision": precision,
            "recall": recall,
            "f1_score": f1,
            "retrieved_count": len(retrieved_ids),
            "relevant_count": len(relevant_chunk_ids),
        }
        
        # Store metrics
        self.metrics["retrieval_precision"].append(precision)
        self.metrics["retrieval_recall"].append(recall)
        
        return metrics
    
    async def evaluate_answer_quality(
        self,
        question: str,
        answer: str,
        context_chunks: List[DocumentChunk],
        ground_truth: Optional[str] = None
    ) -> Dict[str, float]:
        """
        Evaluate answer quality
        
        Args:
            question: Question asked
            answer: Generated answer
            context_chunks: Context used
            ground_truth: Ground truth answer (optional)
            
        Returns:
            Quality metrics
        """
        metrics = {}
        
        # Answer relevance (simplified)
        relevance_score = self._calculate_relevance(question, answer)
        metrics["answer_relevance"] = relevance_score
        
        # Faithfulness (answer grounded in context)
        faithfulness_score = self._calculate_faithfulness(answer, context_chunks)
        metrics["faithfulness"] = faithfulness_score
        
        # Context relevance
        context_relevance = self._calculate_context_relevance(question, context_chunks)
        metrics["context_relevance"] = context_relevance
        
        # If ground truth available, calculate similarity
        if ground_truth:
            similarity = self._calculate_text_similarity(answer, ground_truth)
            metrics["ground_truth_similarity"] = similarity
        
        # Store metrics
        self.metrics["answer_relevance"].append(relevance_score)
        self.metrics["faithfulness"].append(faithfulness_score)
        self.metrics["context_relevance"].append(context_relevance)
        
        return metrics
    
    def _calculate_relevance(self, question: str, answer: str) -> float:
        """Calculate answer relevance to question (simplified)"""
        # In production, use semantic similarity
        question_words = set(question.lower().split())
        answer_words = set(answer.lower().split())
        overlap = len(question_words & answer_words)
        return min(overlap / len(question_words), 1.0) if question_words else 0.0
    
    def _calculate_faithfulness(self, answer: str, context_chunks: List[DocumentChunk]) -> float:
        """Calculate faithfulness (answer grounded in context)"""
        # Simplified: check if answer content appears in context
        context_text = " ".join(c.content for c in context_chunks).lower()
        answer_sentences = answer.split('.')
        
        grounded_sentences = sum(
            1 for sent in answer_sentences
            if any(word in context_text for word in sent.lower().split())
        )
        
        return grounded_sentences / len(answer_sentences) if answer_sentences else 0.0
    
    def _calculate_context_relevance(self, question: str, context_chunks: List[DocumentChunk]) -> float:
        """Calculate context relevance to question"""
        if not context_chunks:
            return 0.0
        
        question_words = set(question.lower().split())
        relevance_scores = []
        
        for chunk in context_chunks:
            chunk_words = set(chunk.content.lower().split())
            overlap = len(question_words & chunk_words)
            score = overlap / len(question_words) if question_words else 0.0
            relevance_scores.append(score)
        
        return sum(relevance_scores) / len(relevance_scores)
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity (simplified)"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        return intersection / union if union > 0 else 0.0
    
    def get_evaluation_summary(self) -> Dict[str, Any]:
        """Get summary of evaluation metrics"""
        summary = {}
        
        for metric_name, values in self.metrics.items():
            if values:
                summary[metric_name] = {
                    "mean": sum(values) / len(values),
                    "min": min(values),
                    "max": max(values),
                    "count": len(values),
                }
        
        return summary


# Made with ❤️ by Bob

# Made with Bob
