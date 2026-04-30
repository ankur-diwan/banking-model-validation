import React from 'react';
import { Box, Typography, Container, Paper } from '@mui/material';
import ScenarioBuilder from '../components/StressTesting/ScenarioBuilder';

const StressTestingPage = () => {
  return (
    <Container maxWidth="xl">
      <Paper sx={{ p: 3, mb: 3 }}>
      <ScenarioBuilder />
      </Paper>
    </Container>
  );
};

export default StressTestingPage;
