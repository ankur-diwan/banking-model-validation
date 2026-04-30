import React from 'react';
import { Box, Typography, Container, Paper } from '@mui/material';
import ModelVersions from '../components/Models/ModelVersions';

const ModelVersionsPage = () => {
  return (
    <Container maxWidth="xl">
      <Paper sx={{ p: 3, mb: 3 }}>
      <ModelVersions />
      </Paper>
    </Container>
  );
};

export default ModelVersionsPage;
