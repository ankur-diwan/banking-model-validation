import React from 'react';
import { Box, Typography, Container, Paper } from '@mui/material';
import CustomTestExecution from '../components/CustomTests/CustomTestExecution';

const ExecuteTestsPage = () => {
  return (
    <Container maxWidth="xl">
      <Paper sx={{ p: 3, mb: 3 }}>
      <CustomTestExecution />
      </Paper>
    </Container>
  );
};

export default ExecuteTestsPage;
