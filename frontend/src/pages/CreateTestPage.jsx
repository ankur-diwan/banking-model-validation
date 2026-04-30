import React from 'react';
import { Box, Typography, Container, Paper } from '@mui/material';
import CustomTestBuilder from '../components/CustomTests/CustomTestBuilder';

const CreateTestPage = () => {
  return (
    <Container maxWidth="xl">
      <Paper sx={{ p: 3, mb: 3 }}>
      <CustomTestBuilder />
      </Paper>
    </Container>
  );
};

export default CreateTestPage;
