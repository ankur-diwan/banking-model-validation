import React from 'react';
import { Box, Typography, Container, Paper } from '@mui/material';
import AlertManagement from '../components/Monitoring/AlertManagement';

const AlertsPage = () => {
  return (
    <Container maxWidth="xl">
      <Paper sx={{ p: 3, mb: 3 }}>
      <AlertManagement />
      </Paper>
    </Container>
  );
};

export default AlertsPage;
