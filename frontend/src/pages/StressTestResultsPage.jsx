import React from 'react';
import { Box, Typography, Container, Paper } from '@mui/material';
import StressTestResults from '../components/StressTesting/StressTestResults';

const StressTestResultsPage = () => {
  return (
    <Container maxWidth="xl">
      <Paper sx={{ p: 3, mb: 3 }}>
      <StressTestResults />
      </Paper>
    </Container>
  );
};

export default StressTestResultsPage;
