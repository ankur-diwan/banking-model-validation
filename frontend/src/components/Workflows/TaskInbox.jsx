import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Tabs,
  Tab,
  Badge,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Alert,
  Snackbar
} from '@mui/material';
import {
  Inbox as InboxIcon,
  CheckCircle as ApprovedIcon,
  Cancel as RejectedIcon,
  Schedule as PendingIcon
} from '@mui/icons-material';
import { DataTable, StatusBadge } from '../Shared';
import ApprovalInterface from './ApprovalInterface';
import { orchestrateAPI } from '../../services/api';
import { useStore } from '../../store/useStore';

/**
 * Task inbox for managers to view and manage approval tasks
 */
const TaskInbox = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedTask, setSelectedTask] = useState(null);
  const [approvalDialogOpen, setApprovalDialogOpen] = useState(false);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });
  
  const { user } = useStore();

  // Fetch tasks
  const fetchTasks = async (status = null) => {
    setLoading(true);
    try {
      const response = await orchestrateAPI.getTasks(status);
      setTasks(response.data || []);
    } catch (error) {
      console.error('Error fetching tasks:', error);
      setSnackbar({
        open: true,
        message: 'Failed to fetch tasks',
        severity: 'error'
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const statusMap = ['pending', 'approved', 'rejected'];
    fetchTasks(statusMap[activeTab]);
  }, [activeTab]);

  // Handle tab change
  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  // Handle task click
  const handleTaskClick = (task) => {
    setSelectedTask(task);
    setApprovalDialogOpen(true);
  };

  // Handle approval/rejection
  const handleApprovalAction = async (action, comment) => {
    try {
      await orchestrateAPI.approveTask({
        task_id: selectedTask.id,
        approver: user.email,
        action,
        comment
      });

      setSnackbar({
        open: true,
        message: `Task ${action === 'approve' ? 'approved' : 'rejected'} successfully`,
        severity: 'success'
      });

      setApprovalDialogOpen(false);
      setSelectedTask(null);
      
      // Refresh tasks
      const statusMap = ['pending', 'approved', 'rejected'];
      fetchTasks(statusMap[activeTab]);
    } catch (error) {
      console.error('Error processing approval:', error);
      setSnackbar({
        open: true,
        message: 'Failed to process approval',
        severity: 'error'
      });
    }
  };

  // Filter tasks by status
  const pendingTasks = tasks.filter(t => t.status === 'pending');
  const approvedTasks = tasks.filter(t => t.status === 'approved');
  const rejectedTasks = tasks.filter(t => t.status === 'rejected');

  // Table columns
  const columns = [
    {
      id: 'task_type',
      label: 'Type',
      render: (value) => (
        <Typography variant="body2" sx={{ fontWeight: 500 }}>
          {value.replace(/_/g, ' ').toUpperCase()}
        </Typography>
      )
    },
    {
      id: 'title',
      label: 'Title',
      render: (value) => (
        <Typography variant="body2">{value}</Typography>
      )
    },
    {
      id: 'workflow_id',
      label: 'Workflow',
      render: (value) => (
        <Typography variant="body2" color="text.secondary">
          {value}
        </Typography>
      )
    },
    {
      id: 'priority',
      label: 'Priority',
      render: (value) => (
        <StatusBadge
          status={value}
          variant="outlined"
          tooltip={`Priority: ${value}`}
        />
      )
    },
    {
      id: 'created_at',
      label: 'Created',
      render: (value) => (
        <Typography variant="body2" color="text.secondary">
          {new Date(value).toLocaleDateString()}
        </Typography>
      )
    },
    {
      id: 'status',
      label: 'Status',
      render: (value) => <StatusBadge status={value} />
    }
  ];

  // Get current tasks based on active tab
  const getCurrentTasks = () => {
    switch (activeTab) {
      case 0:
        return pendingTasks;
      case 1:
        return approvedTasks;
      case 2:
        return rejectedTasks;
      default:
        return [];
    }
  };

  return (
    <Box>
      {/* Header */}
      <Box sx={{ mb: 3 }}>
        <Typography variant="h4" gutterBottom>
          Task Inbox
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Review and approve pending tasks
        </Typography>
      </Box>

      {/* Tabs */}
      <Paper sx={{ mb: 2 }}>
        <Tabs
          value={activeTab}
          onChange={handleTabChange}
          indicatorColor="primary"
          textColor="primary"
        >
          <Tab
            icon={
              <Badge badgeContent={pendingTasks.length} color="primary">
                <PendingIcon />
              </Badge>
            }
            label="Pending"
            iconPosition="start"
          />
          <Tab
            icon={
              <Badge badgeContent={approvedTasks.length} color="success">
                <ApprovedIcon />
              </Badge>
            }
            label="Approved"
            iconPosition="start"
          />
          <Tab
            icon={
              <Badge badgeContent={rejectedTasks.length} color="error">
                <RejectedIcon />
              </Badge>
            }
            label="Rejected"
            iconPosition="start"
          />
        </Tabs>
      </Paper>

      {/* Tasks Table */}
      <DataTable
        columns={columns}
        data={getCurrentTasks()}
        onRowClick={handleTaskClick}
        title={`${activeTab === 0 ? 'Pending' : activeTab === 1 ? 'Approved' : 'Rejected'} Tasks`}
        searchable={true}
        exportable={true}
        selectable={false}
      />

      {/* Approval Dialog */}
      <Dialog
        open={approvalDialogOpen}
        onClose={() => setApprovalDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          Task Approval
        </DialogTitle>
        <DialogContent>
          {selectedTask && (
            <ApprovalInterface
              task={selectedTask}
              onApprove={(comment) => handleApprovalAction('approve', comment)}
              onReject={(comment) => handleApprovalAction('reject', comment)}
              onCancel={() => setApprovalDialogOpen(false)}
            />
          )}
        </DialogContent>
      </Dialog>

      {/* Snackbar for notifications */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
      >
        <Alert
          onClose={() => setSnackbar({ ...snackbar, open: false })}
          severity={snackbar.severity}
          sx={{ width: '100%' }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default TaskInbox;

// Made with Bob
