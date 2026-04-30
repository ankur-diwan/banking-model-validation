import React from 'react';
import { Box, Typography, Container, Paper } from '@mui/material';


const SettingsPage = () => {
  return (
    <Container maxWidth="xl">
      <Paper sx={{ p: 3, mb: 3 }}>
      <Box sx={{ textAlign: 'center', py: 8 }}>
        <Typography variant="h4" gutterBottom>
          Settings
        </Typography>
        <Typography variant="body1" color="text.secondary" paragraph>
          Application settings and preferences
        </Typography>
        <Typography variant="body2" color="text.secondary">
          This page is under development.
        </Typography>
      </Box>
      </Paper>
    </Container>
  );
};

export default SettingsPage;
