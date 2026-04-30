import React from 'react';
import { Box, Typography, Container, Paper } from '@mui/material';
import HelpCenter from '../components/SmartHelp/HelpCenter';

const HelpCenterPage = () => {
  return (
    <Container maxWidth="xl">
      <Paper sx={{ p: 3, mb: 3 }}>
      <HelpCenter />
      </Paper>
    </Container>
  );
};

export default HelpCenterPage;
