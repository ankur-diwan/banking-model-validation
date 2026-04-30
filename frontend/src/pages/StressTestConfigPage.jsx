import React from 'react';
import { Box, Typography, Container, Paper } from '@mui/material';
import StressTestConfig from '../components/StressTesting/StressTestConfig';

const StressTestConfigPage = () => {
  return (
    <Container maxWidth="xl">
      <Paper sx={{ p: 3, mb: 3 }}>
      <StressTestConfig />
      </Paper>
    </Container>
  );
};

export default StressTestConfigPage;
