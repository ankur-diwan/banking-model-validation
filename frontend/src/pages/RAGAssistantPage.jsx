import React from 'react';
import { Box, Typography, Container, Paper } from '@mui/material';
import RAGAssistant from '../components/RAG/RAGAssistant';

const RAGAssistantPage = () => {
  return (
    <Container maxWidth="xl">
      <Paper sx={{ p: 3, mb: 3 }}>
      <RAGAssistant />
      </Paper>
    </Container>
  );
};

export default RAGAssistantPage;
