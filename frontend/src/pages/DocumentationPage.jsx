import React from 'react';
import { Box, Typography, Container, Paper } from '@mui/material';
import DocumentViewer from '../components/RAG/DocumentViewer';

const DocumentationPage = () => {
  return (
    <Container maxWidth="xl">
      <Paper sx={{ p: 3, mb: 3 }}>
      <DocumentViewer />
      </Paper>
    </Container>
  );
};

export default DocumentationPage;
