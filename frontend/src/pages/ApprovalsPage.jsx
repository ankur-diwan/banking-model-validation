import React from 'react';
import { Box, Typography, Container, Paper } from '@mui/material';
import ApprovalInterface from '../components/Workflows/ApprovalInterface';

const ApprovalsPage = () => {
  return (
    <Container maxWidth="xl">
      <Paper sx={{ p: 3, mb: 3 }}>
      <ApprovalInterface />
      </Paper>
    </Container>
  );
};

export default ApprovalsPage;
