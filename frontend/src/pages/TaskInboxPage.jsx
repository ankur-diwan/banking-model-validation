import React from 'react';
import { Box, Typography, Container, Paper } from '@mui/material';
import TaskInbox from '../components/Workflows/TaskInbox';

const TaskInboxPage = () => {
  return (
    <Container maxWidth="xl">
      <Paper sx={{ p: 3, mb: 3 }}>
      <TaskInbox />
      </Paper>
    </Container>
  );
};

export default TaskInboxPage;
