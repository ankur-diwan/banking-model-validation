import React from 'react';
import { Box, Typography, Container, Paper } from '@mui/material';
import DriftDetection from '../components/Monitoring/DriftDetection';

const DriftDetectionPage = () => {
  return (
    <Container maxWidth="xl">
      <Paper sx={{ p: 3, mb: 3 }}>
      <DriftDetection />
      </Paper>
    </Container>
  );
};

export default DriftDetectionPage;
