import React from 'react';
import { Box, Typography, Container, Paper } from '@mui/material';
import MonitoringDashboard from '../components/Monitoring/MonitoringDashboard';

const MonitoringDashboardPage = () => {
  return (
    <Container maxWidth="xl">
      <Paper sx={{ p: 3, mb: 3 }}>
      <MonitoringDashboard />
      </Paper>
    </Container>
  );
};

export default MonitoringDashboardPage;
