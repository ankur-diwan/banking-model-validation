import React from 'react';
import { Box, Typography, Container, Paper } from '@mui/material';


const NotFoundPage = () => {
  return (
    <Container maxWidth="xl">
      <Paper sx={{ p: 3, mb: 3 }}>
      <Box sx={{ textAlign: 'center', py: 8 }}>
        <Typography variant="h4" gutterBottom>
          404 - Page Not Found
        </Typography>
        <Typography variant="body1" color="text.secondary" paragraph>
          The page you are looking for does not exist
        </Typography>
        <Typography variant="body2" color="text.secondary">
          This page is under development.
        </Typography>
      </Box>
      </Paper>
    </Container>
  );
};

export default NotFoundPage;
