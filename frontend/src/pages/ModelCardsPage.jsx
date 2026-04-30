import React from 'react';
import { Box, Typography, Container, Paper } from '@mui/material';
import ModelCards from '../components/Compliance/ModelCards';

const ModelCardsPage = () => {
  return (
    <Container maxWidth="xl">
      <Paper sx={{ p: 3, mb: 3 }}>
      <ModelCards />
      </Paper>
    </Container>
  );
};

export default ModelCardsPage;
