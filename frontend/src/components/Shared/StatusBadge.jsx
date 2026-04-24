import React from 'react';
import { Chip, Tooltip } from '@mui/material';
import {
  CheckCircle as SuccessIcon,
  Error as ErrorIcon,
  Warning as WarningIcon,
  Info as InfoIcon,
  HourglassEmpty as PendingIcon,
  PlayArrow as RunningIcon,
  Cancel as CancelledIcon,
  Schedule as ScheduledIcon
} from '@mui/icons-material';

/**
 * Standardized status badge component with consistent styling
 * 
 * @param {Object} props
 * @param {String} props.status - Status value
 * @param {String} props.variant - Badge variant (default, outlined)
 * @param {String} props.size - Badge size (small, medium)
 * @param {Boolean} props.showIcon - Show status icon
 * @param {String} props.tooltip - Tooltip text
 */
const StatusBadge = ({
  status,
  variant = 'default',
  size = 'small',
  showIcon = true,
  tooltip
}) => {
  // Status configurations
  const statusConfig = {
    // Validation statuses
    passed: {
      label: 'Passed',
      color: 'success',
      icon: <SuccessIcon fontSize="small" />
    },
    failed: {
      label: 'Failed',
      color: 'error',
      icon: <ErrorIcon fontSize="small" />
    },
    warning: {
      label: 'Warning',
      color: 'warning',
      icon: <WarningIcon fontSize="small" />
    },
    pending: {
      label: 'Pending',
      color: 'default',
      icon: <PendingIcon fontSize="small" />
    },
    running: {
      label: 'Running',
      color: 'info',
      icon: <RunningIcon fontSize="small" />
    },
    
    // Model statuses
    active: {
      label: 'Active',
      color: 'success',
      icon: <SuccessIcon fontSize="small" />
    },
    inactive: {
      label: 'Inactive',
      color: 'default',
      icon: <InfoIcon fontSize="small" />
    },
    deprecated: {
      label: 'Deprecated',
      color: 'warning',
      icon: <WarningIcon fontSize="small" />
    },
    retired: {
      label: 'Retired',
      color: 'error',
      icon: <CancelledIcon fontSize="small" />
    },
    
    // Workflow statuses
    approved: {
      label: 'Approved',
      color: 'success',
      icon: <SuccessIcon fontSize="small" />
    },
    rejected: {
      label: 'Rejected',
      color: 'error',
      icon: <ErrorIcon fontSize="small" />
    },
    'in-review': {
      label: 'In Review',
      color: 'info',
      icon: <RunningIcon fontSize="small" />
    },
    draft: {
      label: 'Draft',
      color: 'default',
      icon: <InfoIcon fontSize="small" />
    },
    
    // Deployment statuses
    deployed: {
      label: 'Deployed',
      color: 'success',
      icon: <SuccessIcon fontSize="small" />
    },
    deploying: {
      label: 'Deploying',
      color: 'info',
      icon: <RunningIcon fontSize="small" />
    },
    'deployment-failed': {
      label: 'Deployment Failed',
      color: 'error',
      icon: <ErrorIcon fontSize="small" />
    },
    scheduled: {
      label: 'Scheduled',
      color: 'default',
      icon: <ScheduledIcon fontSize="small" />
    },
    
    // Monitoring statuses
    healthy: {
      label: 'Healthy',
      color: 'success',
      icon: <SuccessIcon fontSize="small" />
    },
    degraded: {
      label: 'Degraded',
      color: 'warning',
      icon: <WarningIcon fontSize="small" />
    },
    critical: {
      label: 'Critical',
      color: 'error',
      icon: <ErrorIcon fontSize="small" />
    },
    unknown: {
      label: 'Unknown',
      color: 'default',
      icon: <InfoIcon fontSize="small" />
    },
    
    // Compliance statuses
    compliant: {
      label: 'Compliant',
      color: 'success',
      icon: <SuccessIcon fontSize="small" />
    },
    'non-compliant': {
      label: 'Non-Compliant',
      color: 'error',
      icon: <ErrorIcon fontSize="small" />
    },
    'needs-review': {
      label: 'Needs Review',
      color: 'warning',
      icon: <WarningIcon fontSize="small" />
    },
    
    // Task statuses
    completed: {
      label: 'Completed',
      color: 'success',
      icon: <SuccessIcon fontSize="small" />
    },
    'in-progress': {
      label: 'In Progress',
      color: 'info',
      icon: <RunningIcon fontSize="small" />
    },
    cancelled: {
      label: 'Cancelled',
      color: 'default',
      icon: <CancelledIcon fontSize="small" />
    },
    
    // Test statuses
    success: {
      label: 'Success',
      color: 'success',
      icon: <SuccessIcon fontSize="small" />
    },
    error: {
      label: 'Error',
      color: 'error',
      icon: <ErrorIcon fontSize="small" />
    },
    skipped: {
      label: 'Skipped',
      color: 'default',
      icon: <InfoIcon fontSize="small" />
    }
  };

  // Get configuration for the status
  const config = statusConfig[status?.toLowerCase()] || {
    label: status || 'Unknown',
    color: 'default',
    icon: <InfoIcon fontSize="small" />
  };

  const badge = (
    <Chip
      label={config.label}
      color={config.color}
      size={size}
      variant={variant === 'outlined' ? 'outlined' : 'filled'}
      icon={showIcon ? config.icon : undefined}
      sx={{
        fontWeight: 500,
        ...(variant === 'outlined' && {
          borderWidth: 2
        })
      }}
    />
  );

  // Wrap with tooltip if provided
  if (tooltip) {
    return <Tooltip title={tooltip}>{badge}</Tooltip>;
  }

  return badge;
};

export default StatusBadge;

// Made with Bob
