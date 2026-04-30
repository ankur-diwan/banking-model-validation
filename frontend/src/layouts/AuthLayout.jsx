import React from 'react';
import { Outlet } from 'react-router-dom';
import { Box, Container, Paper, Typography } from '@mui/material';
import AccountBalanceIcon from '@mui/icons-material/AccountBalance';

const AuthLayout = () => {
  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        py: 4,
      }}
    >
      <Container maxWidth="sm">
        <Paper
          elevation={6}
          sx={{
            p: 4,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            borderRadius: 2,
          }}
        >
          {/* Logo and Title */}
          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              mb: 3,
            }}
          >
            <AccountBalanceIcon
              sx={{
                fontSize: 48,
                color: 'primary.main',
                mr: 2,
              }}
            />
            <Box>
              <Typography variant="h4" component="h1" fontWeight="bold">
                Banking Model
              </Typography>
              <Typography variant="h6" color="text.secondary">
                Validation System
              </Typography>
            </Box>
          </Box>

          {/* Auth Form Content */}
          <Box sx={{ width: '100%' }}>
            <Outlet /> {/* Login/Register forms render here */}
          </Box>

          {/* Footer */}
          <Typography
            variant="caption"
            color="text.secondary"
            sx={{ mt: 4, textAlign: 'center' }}
          >
            © 2026 Banking Model Validation System. All rights reserved.
            <br />
            Powered by IBM watsonx
          </Typography>
        </Paper>
      </Container>
    </Box>
  );
};

export default AuthLayout;

// Made with Bob
