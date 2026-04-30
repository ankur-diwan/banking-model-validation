import React from 'react';
import { Box, Typography, Container, Paper } from '@mui/material';
import ModelInventory from '../components/Models/ModelInventory';

const ModelInventoryPage = () => {
  return (
    <Container maxWidth="xl">
      <Paper sx={{ p: 3, mb: 3 }}>
      <ModelInventory />
      </Paper>
    </Container>
  );
};

export default ModelInventoryPage;
