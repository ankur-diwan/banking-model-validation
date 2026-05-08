/**
 * ValidationResults Component - Simplified and Error-Safe
 * Displays comprehensive validation results
 */

import React from 'react';
import {
  Box,
  Paper,
  Typography,
  Grid,
  Card,
  CardContent,
  Chip,
  Alert,
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from '@mui/material';
import {
  CheckCircle,
  Warning,
  Error as ErrorIcon,
  ExpandMore,
} from '@mui/icons-material';

const ValidationResults = ({ results }) => {
  console.log('=== ValidationResults Rendering ===');
  console.log('Results:', results);

  if (!results) {
    return (
      <Alert severity="info">
        No validation results available. Please run a validation first.
      </Alert>
    );
  }

  // Safe accessor helper
  const safeGet = (obj, path, defaultValue = 'N/A') => {
    try {
      const value = path.split('.').reduce((acc, part) => acc?.[part], obj);
      return value !== undefined && value !== null ? value : defaultValue;
    } catch (e) {
      return defaultValue;
    }
  };

  // Format number safely
  const formatNumber = (value, decimals = 4) => {
    if (value === null || value === undefined || isNaN(value)) return 'N/A';
    return Number(value).toFixed(decimals);
  };

  // Format percentage safely
  const formatPercent = (value) => {
    if (value === null || value === undefined || isNaN(value)) return 'N/A';
    return `${(value * 100).toFixed(2)}%`;
  };

  // Get status color
  const getStatusColor = (status) => {
    const statusLower = String(status).toLowerCase();
    if (statusLower.includes('pass') || statusLower.includes('stable')) return 'success';
    if (statusLower.includes('warn') || statusLower.includes('moderate')) return 'warning';
    if (statusLower.includes('fail') || statusLower.includes('unstable')) return 'error';
    return 'default';
  };

  return (
    <Box sx={{ mt: 3 }}>
      {/* Overall Summary */}
      <Card sx={{ mb: 3, bgcolor: 'primary.light', color: 'primary.contrastText' }}>
        <CardContent>
          <Typography variant="h5" gutterBottom>
            Validation Summary
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} md={3}>
              <Typography variant="body2">Overall Status</Typography>
              <Chip
                label={safeGet(results, 'summary.overall_status', 'UNKNOWN')}
                color={getStatusColor(safeGet(results, 'summary.overall_status'))}
                sx={{ mt: 1 }}
              />
            </Grid>
            <Grid item xs={12} md={3}>
              <Typography variant="body2">KS Statistic</Typography>
              <Typography variant="h6">
                {formatNumber(safeGet(results, 'summary.ks_statistic', 0))}
              </Typography>
            </Grid>
            <Grid item xs={12} md={3}>
              <Typography variant="body2">Gini Coefficient</Typography>
              <Typography variant="h6">
                {formatNumber(safeGet(results, 'summary.gini_coefficient', 0))}
              </Typography>
            </Grid>
            <Grid item xs={12} md={3}>
              <Typography variant="body2">Compliance Score</Typography>
              <Typography variant="h6">
                {formatNumber(safeGet(results, 'summary.compliance_score', 0), 2)}%
              </Typography>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Statistical Tests */}
      <Accordion defaultExpanded>
        <AccordionSummary expandIcon={<ExpandMore />}>
          <Typography variant="h6">📊 Statistical Tests</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Grid container spacing={2}>
            {/* Train Dataset */}
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Typography variant="subtitle1" gutterBottom>
                    Train Dataset
                  </Typography>
                  <Typography variant="body2">
                    KS: {formatNumber(safeGet(results, 'statistical_tests.train.ks_statistic', 0))}
                  </Typography>
                  <Typography variant="body2">
                    Gini: {formatNumber(safeGet(results, 'statistical_tests.train.gini_coefficient', 0))}
                  </Typography>
                  <Typography variant="body2">
                    PSI: {formatNumber(safeGet(results, 'statistical_tests.train.psi', 0))}
                  </Typography>
                  <Typography variant="body2">
                    CSI: {formatNumber(safeGet(results, 'statistical_tests.train.csi', 0))}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>

            {/* Test Dataset */}
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Typography variant="subtitle1" gutterBottom>
                    Test Dataset
                  </Typography>
                  <Typography variant="body2">
                    KS: {formatNumber(safeGet(results, 'statistical_tests.test.ks_statistic', 0))}
                  </Typography>
                  <Typography variant="body2">
                    Gini: {formatNumber(safeGet(results, 'statistical_tests.test.gini_coefficient', 0))}
                  </Typography>
                  <Typography variant="body2">
                    PSI: {formatNumber(safeGet(results, 'statistical_tests.test.psi', 0))}
                  </Typography>
                  <Typography variant="body2">
                    CSI: {formatNumber(safeGet(results, 'statistical_tests.test.csi', 0))}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>

            {/* OOT Dataset */}
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Typography variant="subtitle1" gutterBottom>
                    Out-of-Time
                  </Typography>
                  <Typography variant="body2">
                    KS: {formatNumber(safeGet(results, 'statistical_tests.out_of_time.ks_statistic', 0))}
                  </Typography>
                  <Typography variant="body2">
                    Gini: {formatNumber(safeGet(results, 'statistical_tests.out_of_time.gini_coefficient', 0))}
                  </Typography>
                  <Typography variant="body2">
                    PSI: {formatNumber(safeGet(results, 'statistical_tests.out_of_time.psi', 0))}
                  </Typography>
                  <Typography variant="body2">
                    CSI: {formatNumber(safeGet(results, 'statistical_tests.out_of_time.csi', 0))}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </AccordionDetails>
      </Accordion>

      {/* Performance Metrics */}
      <Accordion>
        <AccordionSummary expandIcon={<ExpandMore />}>
          <Typography variant="h6">📈 Performance Metrics</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Grid container spacing={2}>
            {['train', 'test', 'out_of_time'].map((dataset) => (
              <Grid item xs={12} md={4} key={dataset}>
                <Card>
                  <CardContent>
                    <Typography variant="subtitle1" gutterBottom>
                      {dataset === 'out_of_time' ? 'Out-of-Time' : dataset.charAt(0).toUpperCase() + dataset.slice(1)}
                    </Typography>
                    <Typography variant="body2">
                      Accuracy: {formatPercent(safeGet(results, `performance.${dataset}.accuracy`, 0))}
                    </Typography>
                    <Typography variant="body2">
                      Precision: {formatPercent(safeGet(results, `performance.${dataset}.precision`, 0))}
                    </Typography>
                    <Typography variant="body2">
                      Recall: {formatPercent(safeGet(results, `performance.${dataset}.recall`, 0))}
                    </Typography>
                    <Typography variant="body2">
                      F1 Score: {formatPercent(safeGet(results, `performance.${dataset}.f1_score`, 0))}
                    </Typography>
                    <Typography variant="body2">
                      AUC-ROC: {formatNumber(safeGet(results, `performance.${dataset}.auc_roc`, 0))}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </AccordionDetails>
      </Accordion>

      {/* Compliance */}
      <Accordion>
        <AccordionSummary expandIcon={<ExpandMore />}>
          <Typography variant="h6">✅ SR 11-7 Compliance</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Box>
            <Alert severity={getStatusColor(safeGet(results, 'compliance.overall_status'))} sx={{ mb: 2 }}>
              <Typography variant="body1">
                <strong>Status:</strong> {safeGet(results, 'compliance.overall_status', 'Unknown')}
              </Typography>
              <Typography variant="body1">
                <strong>Score:</strong> {formatNumber(safeGet(results, 'compliance.compliance_score', 0), 2)}%
              </Typography>
              <Typography variant="body1">
                <strong>SR 11-7 Compliant:</strong> {safeGet(results, 'compliance.sr_11_7_compliant', false) ? 'Yes' : 'No'}
              </Typography>
            </Alert>

            {/* Detailed Checks */}
            {results.compliance?.detailed_checks && (
              <Box sx={{ mt: 2 }}>
                <Typography variant="subtitle1" gutterBottom>
                  Detailed Checks
                </Typography>
                <Grid container spacing={1}>
                  {Object.entries(results.compliance.detailed_checks).map(([key, check]) => (
                    <Grid item xs={12} sm={6} md={4} key={key}>
                      <Card variant="outlined">
                        <CardContent>
                          <Typography variant="body2" gutterBottom>
                            {check.description || key}
                          </Typography>
                          <Chip
                            label={check.status || 'Unknown'}
                            color={getStatusColor(check.status)}
                            size="small"
                          />
                          <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                            Score: {formatNumber(check.score || 0, 2)} / {check.weight || 0}
                          </Typography>
                        </CardContent>
                      </Card>
                    </Grid>
                  ))}
                </Grid>
              </Box>
            )}

            {/* Recommendations */}
            {results.compliance?.recommendations && results.compliance.recommendations.length > 0 && (
              <Box sx={{ mt: 3 }}>
                <Typography variant="subtitle1" gutterBottom>
                  Recommendations
                </Typography>
                {results.compliance.recommendations.map((rec, idx) => (
                  <Alert severity="info" key={idx} sx={{ mb: 1 }}>
                    {rec}
                  </Alert>
                ))}
              </Box>
            )}
          </Box>
        </AccordionDetails>
      </Accordion>

      {/* Model Specific */}
      {results.model_specific && (
        <Accordion>
          <AccordionSummary expandIcon={<ExpandMore />}>
            <Typography variant="h6">🎯 Model-Specific Validation</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Typography variant="body2">
              <strong>Validation Type:</strong> {safeGet(results, 'model_specific.validation_type', 'N/A')}
            </Typography>
            <Typography variant="body2">
              <strong>Use Case:</strong> {safeGet(results, 'model_specific.use_case', 'N/A')}
            </Typography>
            <Typography variant="body2">
              <strong>Status:</strong>{' '}
              <Chip
                label={safeGet(results, 'model_specific.status', 'Unknown')}
                color={getStatusColor(safeGet(results, 'model_specific.status'))}
                size="small"
              />
            </Typography>
          </AccordionDetails>
        </Accordion>
      )}
    </Box>
  );
};

export default ValidationResults;

// Made with Bob
