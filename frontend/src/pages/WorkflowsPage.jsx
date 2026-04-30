import React from 'react';
import { Box, Typography, Container, Paper } from '@mui/material';
import WorkflowList from '../components/Workflows/WorkflowList';

const WorkflowsPage = () => {
  return (
    <Container maxWidth="xl">
      <Paper sx={{ p: 3, mb: 3 }}>
      <WorkflowList />
      </Paper>
    </Container>
  );
};

export default WorkflowsPage;
