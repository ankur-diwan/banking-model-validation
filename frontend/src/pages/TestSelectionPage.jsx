import React from 'react';
import { Box, Typography, Container, Paper } from '@mui/material';
import TestSelection from '../components/Validation/TestSelection';

const TestSelectionPage = () => {
  return (
    <Container maxWidth="xl">
      <Paper sx={{ p: 3, mb: 3 }}>
      <TestSelection />
      </Paper>
    </Container>
  );
};

export default TestSelectionPage;
