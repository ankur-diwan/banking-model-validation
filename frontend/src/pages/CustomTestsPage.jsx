import React from 'react';
import { Box, Typography, Container, Paper } from '@mui/material';
import TestLibrary from '../components/CustomTests/TestLibrary';

const CustomTestsPage = () => {
  return (
    <Container maxWidth="xl">
      <Paper sx={{ p: 3, mb: 3 }}>
      <TestLibrary />
      </Paper>
    </Container>
  );
};

export default CustomTestsPage;
