import React from 'react';
import { Box, Typography, Container, Paper } from '@mui/material';
import DocumentationEditor from '../components/RAG/DocumentationEditor';

const DocumentEditorPage = () => {
  return (
    <Container maxWidth="xl">
      <Paper sx={{ p: 3, mb: 3 }}>
      <DocumentationEditor />
      </Paper>
    </Container>
  );
};

export default DocumentEditorPage;
