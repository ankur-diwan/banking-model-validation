import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  Grid,
  Divider,
  Chip,
  Alert,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemText,
  ListItemIcon
} from '@mui/material';
import {
  CheckCircle as ApproveIcon,
  Cancel as RejectIcon,
  Info as InfoIcon,
  Description as DocumentIcon,
  Person as PersonIcon,
  Schedule as TimeIcon,
  Assignment as TaskIcon
} from '@mui/icons-material';
import { StatusBadge } from '../Shared';

/**
 * Approval interface for reviewing and approving/rejecting tasks
 * 
 * @param {Object} props
 * @param {Object} props.task - Task to approve/reject
 * @param {Function} props.onApprove - Approve handler
 * @param {Function} props.onReject - Reject handler
 * @param {Function} props.onCancel - Cancel handler
 */
const ApprovalInterface = ({ task, onApprove, onReject, onCancel }) => {
  const [comment, setComment] = useState('');
  const [error, setError] = useState('');

  const handleApprove = () => {
    if (!comment.trim()) {
      setError('Please provide a comment for approval');
      return;
    }
    onApprove(comment);
  };

  const handleReject = () => {
    if (!comment.trim()) {
      setError('Please provide a reason for rejection');
      return;
    }
    onReject(comment);
  };

  if (!task) {
    return (
      <Alert severity="info">
        No task selected
      </Alert>
    );
  }

  return (
    <Box>
      {/* Task Overview */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', mb: 2 }}>
            <Box>
              <Typography variant="h6" gutterBottom>
                {task.title}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                {task.description}
              </Typography>
            </Box>
            <StatusBadge status={task.status} />
          </Box>

          <Grid container spacing={2} sx={{ mt: 2 }}>
            <Grid item xs={12} sm={6}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <TaskIcon fontSize="small" color="action" />
                <Box>
                  <Typography variant="caption" color="text.secondary">
                    Task Type
                  </Typography>
                  <Typography variant="body2">
                    {task.task_type?.replace(/_/g, ' ').toUpperCase()}
                  </Typography>
                </Box>
              </Box>
            </Grid>

            <Grid item xs={12} sm={6}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <PersonIcon fontSize="small" color="action" />
                <Box>
                  <Typography variant="caption" color="text.secondary">
                    Requester
                  </Typography>
                  <Typography variant="body2">
                    {task.requester || 'N/A'}
                  </Typography>
                </Box>
              </Box>
            </Grid>

            <Grid item xs={12} sm={6}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <TimeIcon fontSize="small" color="action" />
                <Box>
                  <Typography variant="caption" color="text.secondary">
                    Created
                  </Typography>
                  <Typography variant="body2">
                    {new Date(task.created_at).toLocaleString()}
                  </Typography>
                </Box>
              </Box>
            </Grid>

            <Grid item xs={12} sm={6}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <InfoIcon fontSize="small" color="action" />
                <Box>
                  <Typography variant="caption" color="text.secondary">
                    Priority
                  </Typography>
                  <Typography variant="body2">
                    <Chip
                      label={task.priority || 'Normal'}
                      size="small"
                      color={
                        task.priority === 'high' ? 'error' :
                        task.priority === 'medium' ? 'warning' : 'default'
                      }
                    />
                  </Typography>
                </Box>
              </Box>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Task Details */}
      {task.details && (
        <Paper sx={{ p: 2, mb: 3 }}>
          <Typography variant="subtitle2" gutterBottom>
            Task Details
          </Typography>
          <Divider sx={{ mb: 2 }} />
          
          {typeof task.details === 'object' ? (
            <List dense>
              {Object.entries(task.details).map(([key, value]) => (
                <ListItem key={key}>
                  <ListItemIcon>
                    <DocumentIcon fontSize="small" />
                  </ListItemIcon>
                  <ListItemText
                    primary={key.replace(/_/g, ' ').toUpperCase()}
                    secondary={
                      typeof value === 'object'
                        ? JSON.stringify(value, null, 2)
                        : String(value)
                    }
                  />
                </ListItem>
              ))}
            </List>
          ) : (
            <Typography variant="body2" color="text.secondary">
              {task.details}
            </Typography>
          )}
        </Paper>
      )}

      {/* Approval History */}
      {task.approval_history && task.approval_history.length > 0 && (
        <Paper sx={{ p: 2, mb: 3 }}>
          <Typography variant="subtitle2" gutterBottom>
            Approval History
          </Typography>
          <Divider sx={{ mb: 2 }} />
          
          <List dense>
            {task.approval_history.map((entry, index) => (
              <ListItem key={index}>
                <ListItemText
                  primary={
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Typography variant="body2">
                        {entry.approver}
                      </Typography>
                      <StatusBadge status={entry.action} size="small" />
                    </Box>
                  }
                  secondary={
                    <>
                      <Typography variant="caption" display="block">
                        {new Date(entry.timestamp).toLocaleString()}
                      </Typography>
                      {entry.comment && (
                        <Typography variant="body2" sx={{ mt: 0.5 }}>
                          {entry.comment}
                        </Typography>
                      )}
                    </>
                  }
                />
              </ListItem>
            ))}
          </List>
        </Paper>
      )}

      {/* Comment Section */}
      {task.status === 'pending' && (
        <>
          <Paper sx={{ p: 2, mb: 3 }}>
            <Typography variant="subtitle2" gutterBottom>
              Your Decision
            </Typography>
            <Divider sx={{ mb: 2 }} />
            
            <TextField
              fullWidth
              multiline
              rows={4}
              label="Comment"
              placeholder="Provide your comments or reasons for this decision..."
              value={comment}
              onChange={(e) => {
                setComment(e.target.value);
                setError('');
              }}
              error={!!error}
              helperText={error || 'Required for approval or rejection'}
              sx={{ mb: 2 }}
            />

            {error && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {error}
              </Alert>
            )}
          </Paper>

          {/* Action Buttons */}
          <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
            <Button
              variant="outlined"
              onClick={onCancel}
            >
              Cancel
            </Button>
            <Button
              variant="outlined"
              color="error"
              startIcon={<RejectIcon />}
              onClick={handleReject}
            >
              Reject
            </Button>
            <Button
              variant="contained"
              color="success"
              startIcon={<ApproveIcon />}
              onClick={handleApprove}
            >
              Approve
            </Button>
          </Box>
        </>
      )}

      {/* Already Processed */}
      {task.status !== 'pending' && (
        <Alert severity="info">
          This task has already been {task.status}
        </Alert>
      )}
    </Box>
  );
};

export default ApprovalInterface;

// Made with Bob
