import React from 'react';
import { Box, Typography, Container, Paper } from '@mui/material';
import AuditTrail from '../components/Compliance/AuditTrail';

const AuditTrailPage = () => {
  return (
    <Container maxWidth="xl">
      <Paper sx={{ p: 3, mb: 3 }}>
      <AuditTrail />
      </Paper>
    </Container>
  );
};

export default AuditTrailPage;
