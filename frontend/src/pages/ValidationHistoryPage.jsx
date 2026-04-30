import React from 'react';
import { Box, Typography, Container, Paper } from '@mui/material';


const ValidationHistoryPage = () => {
  return (
    <Container maxWidth="xl">
      <Paper sx={{ p: 3, mb: 3 }}>
      <Box sx={{ textAlign: 'center', py: 8 }}>
        <Typography variant="h4" gutterBottom>
          Validation History
        </Typography>
        <Typography variant="body1" color="text.secondary" paragraph>
          View past validation results and reports
        </Typography>
        <Typography variant="body2" color="text.secondary">
          This page is under development.
        </Typography>
      </Box>
      </Paper>
    </Container>
  );
};

export default ValidationHistoryPage;
