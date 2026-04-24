import React, { useState } from 'react';
import {
  Paper,
  Box,
  Typography,
  IconButton,
  Menu,
  MenuItem,
  Tooltip,
  Divider,
  CircularProgress
} from '@mui/material';
import {
  MoreVert as MoreIcon,
  GetApp as DownloadIcon,
  Fullscreen as FullscreenIcon,
  Refresh as RefreshIcon,
  Info as InfoIcon
} from '@mui/icons-material';
import html2canvas from 'html2canvas';

/**
 * Reusable chart container with consistent styling, export, and fullscreen capabilities
 * 
 * @param {Object} props
 * @param {String} props.title - Chart title
 * @param {String} props.subtitle - Chart subtitle
 * @param {React.Node} props.children - Chart component
 * @param {Function} props.onRefresh - Refresh handler
 * @param {Function} props.onFullscreen - Fullscreen handler
 * @param {Boolean} props.loading - Loading state
 * @param {String} props.info - Info tooltip text
 * @param {Array} props.actions - Additional actions
 * @param {String} props.height - Chart height
 */
const ChartContainer = ({
  title,
  subtitle,
  children,
  onRefresh,
  onFullscreen,
  loading = false,
  info,
  actions = [],
  height = '400px',
  exportable = true
}) => {
  const [anchorEl, setAnchorEl] = useState(null);
  const chartRef = React.useRef(null);

  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  // Export chart as PNG
  const handleExportPNG = async () => {
    if (chartRef.current) {
      try {
        const canvas = await html2canvas(chartRef.current, {
          backgroundColor: '#ffffff',
          scale: 2
        });
        const link = document.createElement('a');
        link.download = `${title || 'chart'}_${new Date().toISOString()}.png`;
        link.href = canvas.toDataURL();
        link.click();
      } catch (error) {
        console.error('Error exporting chart:', error);
      }
    }
    handleMenuClose();
  };

  // Export chart as SVG (if supported)
  const handleExportSVG = () => {
    if (chartRef.current) {
      const svgElement = chartRef.current.querySelector('svg');
      if (svgElement) {
        const svgData = new XMLSerializer().serializeToString(svgElement);
        const blob = new Blob([svgData], { type: 'image/svg+xml' });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.download = `${title || 'chart'}_${new Date().toISOString()}.svg`;
        link.href = url;
        link.click();
        window.URL.revokeObjectURL(url);
      }
    }
    handleMenuClose();
  };

  // Export data as CSV
  const handleExportData = () => {
    // This would need to be implemented based on the specific chart data
    // For now, we'll just close the menu
    handleMenuClose();
  };

  return (
    <Paper
      elevation={2}
      sx={{
        p: 2,
        height: '100%',
        display: 'flex',
        flexDirection: 'column'
      }}
    >
      {/* Header */}
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'flex-start',
          mb: 2
        }}
      >
        <Box sx={{ flex: 1 }}>
          <Typography variant="h6" component="div" gutterBottom>
            {title}
          </Typography>
          {subtitle && (
            <Typography variant="body2" color="text.secondary">
              {subtitle}
            </Typography>
          )}
        </Box>

        <Box sx={{ display: 'flex', gap: 0.5 }}>
          {info && (
            <Tooltip title={info}>
              <IconButton size="small">
                <InfoIcon fontSize="small" />
              </IconButton>
            </Tooltip>
          )}

          {onRefresh && (
            <Tooltip title="Refresh">
              <IconButton size="small" onClick={onRefresh}>
                <RefreshIcon fontSize="small" />
              </IconButton>
            </Tooltip>
          )}

          {onFullscreen && (
            <Tooltip title="Fullscreen">
              <IconButton size="small" onClick={onFullscreen}>
                <FullscreenIcon fontSize="small" />
              </IconButton>
            </Tooltip>
          )}

          {(exportable || actions.length > 0) && (
            <>
              <IconButton size="small" onClick={handleMenuOpen}>
                <MoreIcon fontSize="small" />
              </IconButton>
              <Menu
                anchorEl={anchorEl}
                open={Boolean(anchorEl)}
                onClose={handleMenuClose}
              >
                {exportable && [
                  <MenuItem key="png" onClick={handleExportPNG}>
                    <DownloadIcon fontSize="small" sx={{ mr: 1 }} />
                    Export as PNG
                  </MenuItem>,
                  <MenuItem key="svg" onClick={handleExportSVG}>
                    <DownloadIcon fontSize="small" sx={{ mr: 1 }} />
                    Export as SVG
                  </MenuItem>,
                  <MenuItem key="data" onClick={handleExportData}>
                    <DownloadIcon fontSize="small" sx={{ mr: 1 }} />
                    Export Data
                  </MenuItem>
                ]}
                {exportable && actions.length > 0 && <Divider />}
                {actions.map((action, index) => (
                  <MenuItem
                    key={index}
                    onClick={() => {
                      action.onClick();
                      handleMenuClose();
                    }}
                  >
                    {action.icon && (
                      <Box sx={{ mr: 1, display: 'flex' }}>{action.icon}</Box>
                    )}
                    {action.label}
                  </MenuItem>
                ))}
              </Menu>
            </>
          )}
        </Box>
      </Box>

      {/* Chart Content */}
      <Box
        ref={chartRef}
        sx={{
          flex: 1,
          minHeight: height,
          position: 'relative',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center'
        }}
      >
        {loading ? (
          <CircularProgress />
        ) : (
          <Box sx={{ width: '100%', height: '100%' }}>
            {children}
          </Box>
        )}
      </Box>
    </Paper>
  );
};

export default ChartContainer;

// Made with Bob
