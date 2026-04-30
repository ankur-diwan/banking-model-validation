import React from 'react';
import { Box, Typography, Container, Paper } from '@mui/material';
import ModelOnboarding from '../components/Models/ModelOnboarding';

const ModelOnboardingPage = () => {
  return (
    <Container maxWidth="xl">
      <Paper sx={{ p: 3, mb: 3 }}>
      <ModelOnboarding />
      </Paper>
    </Container>
  );
};

export default ModelOnboardingPage;
