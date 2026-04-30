import React from 'react';
import { Box, Typography, Container, Paper } from '@mui/material';
import ComplianceDashboard from '../components/Compliance/ComplianceDashboard';

const ComplianceDashboardPage = () => {
  return (
    <Container maxWidth="xl">
      <Paper sx={{ p: 3, mb: 3 }}>
      <ComplianceDashboard />
      </Paper>
    </Container>
  );
};

export default ComplianceDashboardPage;
