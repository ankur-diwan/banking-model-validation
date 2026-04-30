import React from 'react';
import { Box, Typography, Container, Paper } from '@mui/material';
import OverviewDashboard from '../components/Dashboard/OverviewDashboard';

const DashboardPage = () => {
  return (
    <Container maxWidth="xl">
      <Paper sx={{ p: 3, mb: 3 }}>
      <OverviewDashboard />
      </Paper>
    </Container>
  );
};

export default DashboardPage;
