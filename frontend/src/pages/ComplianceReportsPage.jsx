import React from 'react';
import { Box, Typography, Container, Paper } from '@mui/material';
import ComplianceReports from '../components/Compliance/ComplianceReports';

const ComplianceReportsPage = () => {
  return (
    <Container maxWidth="xl">
      <Paper sx={{ p: 3, mb: 3 }}>
      <ComplianceReports />
      </Paper>
    </Container>
  );
};

export default ComplianceReportsPage;
