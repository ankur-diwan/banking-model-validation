import React from 'react';
import { Box, Typography, Container, Paper } from '@mui/material';
import PerformanceMetrics from '../components/Monitoring/PerformanceMetrics';

const PerformanceMetricsPage = () => {
  return (
    <Container maxWidth="xl">
      <Paper sx={{ p: 3, mb: 3 }}>
      <PerformanceMetrics />
      </Paper>
    </Container>
  );
};

export default PerformanceMetricsPage;
