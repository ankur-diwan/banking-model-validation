/**
 * ValidationResults Component
 * Displays comprehensive validation results including:
 * - Statistical tests (KS, Gini, PSI, CSI)
 * - Performance metrics
 * - Compliance scores
 * - Model-specific validation results
 */

import React from 'react';
import {
  Box,
  Paper,
  Typography,
  Grid,
  Card,
  CardContent,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Divider,
  Alert,
  LinearProgress,
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from '@mui/material';
import {
  CheckCircle,
  Warning,
  Error as ErrorIcon,
  ExpandMore,
  TrendingUp,
  Assessment,
  Security,
  Speed,
} from '@mui/icons-material';

const ValidationResults = ({ results }) => {
  if (!results) {
    return (
      <Alert severity="info">
        No validation results available. Please run a validation first.
      </Alert>
    );
  }

  // Helper function to get status color
  const getStatusColor = (status) => {
    switch (status?.toLowerCase()) {
      case 'passed':
      case 'compliant':
      case 'stable':
        return 'success';
      case 'warning':
      case 'moderate':
        return 'warning';
      case 'failed':
      case 'non-compliant':
      case 'unstable':
        return 'error';
      default:
        return 'default';
    }
  };

  // Helper function to get status icon
  const getStatusIcon = (status) => {
    switch (status?.toLowerCase()) {
      case 'passed':
      case 'compliant':
      case 'stable':
        return <CheckCircle />;
      case 'warning':
      case 'moderate':
        return <Warning />;
      case 'failed':
      case 'non-compliant':
      case 'unstable':
        return <ErrorIcon />;
      default:
        return null;
    }
  };

  // Format percentage
  const formatPercent = (value) => {
    if (value === null || value === undefined) return 'N/A';
    return `${(value * 100).toFixed(2)}%`;
  };

  // Format number
  const formatNumber = (value, decimals = 4) => {
    if (value === null || value === undefined) return 'N/A';
    return typeof value === 'number' ? value.toFixed(decimals) : value;
  };

  return (
    <Box>
      {/* Overall Summary */}
      <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
        <Typography variant="h5" gutterBottom>
          Validation Summary
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} md={3}>
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <Assessment color="primary" sx={{ mr: 1 }} />
                  <Typography variant="subtitle2">Model Type</Typography>
                </Box>
                <Typography variant="h6" sx={{ textTransform: 'capitalize' }}>
                  {results.metadata?.model_type || results.model_specific?.model_type || 'N/A'}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  Scorecard Category
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={3}>
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <Speed color="success" sx={{ mr: 1 }} />
                  <Typography variant="subtitle2">Performance</Typography>
                </Box>
                <Typography variant="h6">
                  {results.performance?.train?.accuracy
                    ? `${(results.performance.train.accuracy * 100).toFixed(1)}%`
                    : 'N/A'}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  Train Accuracy
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={3}>
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <TrendingUp color="info" sx={{ mr: 1 }} />
                  <Typography variant="subtitle2">Stability</Typography>
                </Box>
                <Typography variant="h6" sx={{ textTransform: 'capitalize' }}>
                  {results.stability?.overall_status || 'N/A'}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  Overall Status
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={3}>
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <Security color="warning" sx={{ mr: 1 }} />
                  <Typography variant="subtitle2">Compliance</Typography>
                </Box>
                <Typography variant="h6">
                  {results.compliance?.compliance_score !== undefined && results.compliance?.compliance_score !== null
                    ? `${results.compliance.compliance_score.toFixed(1)}%`
                    : 'N/A'}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  SR 11-7 Score
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Paper>

      {/* Statistical Tests */}
      {results.statistical_tests && (
        <Accordion defaultExpanded>
          <AccordionSummary expandIcon={<ExpandMore />}>
            <Typography variant="h6">📊 Statistical Tests</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Grid container spacing={2}>
              {/* KS Test */}
              {results.statistical_tests.train && (
                <Grid item xs={12} md={6}>
                  <Card>
                    <CardContent>
                      <Typography variant="subtitle1" gutterBottom>
                        Kolmogorov-Smirnov (KS) Test
                      </Typography>
                      <Divider sx={{ my: 1 }} />
                      <Box sx={{ mt: 2 }}>
                        <Typography variant="body2" color="text.secondary">
                          KS Statistic (Train)
                        </Typography>
                        <Typography variant="h5">
                          {formatNumber(results.statistical_tests.train.ks_statistic)}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          {results.statistical_tests.train.interpretation}
                        </Typography>
                      </Box>
                      <Box sx={{ mt: 2 }}>
                        <Chip
                          label={results.statistical_tests.train.status}
                          color={getStatusColor(results.statistical_tests.train.status)}
                          size="small"
                        />
                      </Box>
                    </CardContent>
                  </Card>
                </Grid>
              )}

              {/* Gini Coefficient */}
              {results.statistical_tests.gini_coefficient && (
                <Grid item xs={12} md={6}>
                  <Card>
                    <CardContent>
                      <Typography variant="subtitle1" gutterBottom>
                        Gini Coefficient
                      </Typography>
                      <Divider sx={{ my: 1 }} />
                      <Box sx={{ mt: 2 }}>
                        <Typography variant="body2" color="text.secondary">
                          Gini Score
                        </Typography>
                        <Typography variant="h5">
                          {formatNumber(results.statistical_tests.gini_coefficient.gini)}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          {results.statistical_tests.gini_coefficient.interpretation}
                        </Typography>
                      </Box>
                      <Box sx={{ mt: 2 }}>
                        <Chip
                          label={results.statistical_tests.gini_coefficient.status}
                          color={getStatusColor(results.statistical_tests.gini_coefficient.status)}
                          size="small"
                        />
                      </Box>
                    </CardContent>
                  </Card>
                </Grid>
              )}
            </Grid>
          </AccordionDetails>
        </Accordion>
      )}

      {/* Performance Metrics */}
      {results.performance && (
        <Accordion defaultExpanded>
          <AccordionSummary expandIcon={<ExpandMore />}>
            <Typography variant="h6">📈 Performance Metrics</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <TableContainer>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>Metric</TableCell>
                    <TableCell align="right">Train</TableCell>
                    <TableCell align="right">Test</TableCell>
                    <TableCell align="right">OOT</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {['accuracy', 'precision', 'recall', 'f1_score', 'auc_roc'].map((metric) => (
                    <TableRow key={metric}>
                      <TableCell component="th" scope="row">
                        {metric.replace(/_/g, ' ').toUpperCase()}
                      </TableCell>
                      <TableCell align="right">
                        {formatNumber(results.performance.train?.[metric])}
                      </TableCell>
                      <TableCell align="right">
                        {formatNumber(results.performance.test?.[metric])}
                      </TableCell>
                      <TableCell align="right">
                        {formatNumber(results.performance.out_of_time?.[metric])}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </AccordionDetails>
        </Accordion>
      )}

      {/* Stability Analysis */}
      {results.stability && (
        <Accordion defaultExpanded>
          <AccordionSummary expandIcon={<ExpandMore />}>
            <Typography variant="h6">🔄 Stability Analysis</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Grid container spacing={2}>
              {/* PSI */}
              {results.stability.psi && (
                <Grid item xs={12} md={6}>
                  <Card>
                    <CardContent>
                      <Typography variant="subtitle1" gutterBottom>
                        Population Stability Index (PSI)
                      </Typography>
                      <Divider sx={{ my: 1 }} />
                      <Box sx={{ mt: 2 }}>
                        <Typography variant="body2" color="text.secondary">
                          PSI Score
                        </Typography>
                        <Typography variant="h5">
                          {formatNumber(results.stability.psi.psi_score)}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          {results.stability.psi.interpretation}
                        </Typography>
                      </Box>
                      <Box sx={{ mt: 2 }}>
                        <LinearProgress
                          variant="determinate"
                          value={Math.min(results.stability.psi.psi_score * 100, 100)}
                          color={getStatusColor(results.stability.psi.status)}
                        />
                      </Box>
                      <Box sx={{ mt: 1 }}>
                        <Chip
                          label={results.stability.psi.status}
                          color={getStatusColor(results.stability.psi.status)}
                          size="small"
                        />
                      </Box>
                    </CardContent>
                  </Card>
                </Grid>
              )}

              {/* CSI */}
              {results.stability.csi && (
                <Grid item xs={12} md={6}>
                  <Card>
                    <CardContent>
                      <Typography variant="subtitle1" gutterBottom>
                        Characteristic Stability Index (CSI)
                      </Typography>
                      <Divider sx={{ my: 1 }} />
                      <Box sx={{ mt: 2 }}>
                        <Typography variant="body2" color="text.secondary">
                          Average CSI
                        </Typography>
                        <Typography variant="h5">
                          {formatNumber(results.stability.csi.average_csi)}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          {results.stability.csi.interpretation}
                        </Typography>
                      </Box>
                      <Box sx={{ mt: 2 }}>
                        <LinearProgress
                          variant="determinate"
                          value={Math.min(results.stability.csi.average_csi * 100, 100)}
                          color={getStatusColor(results.stability.csi.status)}
                        />
                      </Box>
                      <Box sx={{ mt: 1 }}>
                        <Chip
                          label={results.stability.csi.status}
                          color={getStatusColor(results.stability.csi.status)}
                          size="small"
                        />
                      </Box>
                    </CardContent>
                  </Card>
                </Grid>
              )}
            </Grid>
          </AccordionDetails>
        </Accordion>
      )}

      {/* SR 11-7 Compliance */}
      {results.compliance && (
        <Accordion defaultExpanded>
          <AccordionSummary expandIcon={<ExpandMore />}>
            <Typography variant="h6">✅ SR 11-7 Compliance</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Box sx={{ mb: 3 }}>
              <Typography variant="subtitle1" gutterBottom>
                Overall Compliance Score
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <Box sx={{ flexGrow: 1 }}>
                  <LinearProgress
                    variant="determinate"
                    value={results.compliance.compliance_score || 0}
                    sx={{ height: 10, borderRadius: 5 }}
                    color={getStatusColor(results.compliance.overall_status)}
                  />
                </Box>
                <Typography variant="h5">
                  {results.compliance.compliance_score?.toFixed(1)}%
                </Typography>
              </Box>
              <Box sx={{ mt: 1 }}>
                <Chip
                  label={results.compliance.overall_status}
                  color={getStatusColor(results.compliance.overall_status)}
                />
              </Box>
              <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                Categories Passed: {results.compliance.categories_passed} / 9
              </Typography>
            </Box>

            {/* Compliance Categories */}
            {results.compliance.category_scores && (
              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Category</TableCell>
                      <TableCell align="right">Score</TableCell>
                      <TableCell align="right">Weight</TableCell>
                      <TableCell align="center">Status</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {Object.entries(results.compliance.category_scores).map(([category, data]) => (
                      <TableRow key={category}>
                        <TableCell component="th" scope="row">
                          {category.replace(/_/g, ' ').toUpperCase()}
                        </TableCell>
                        <TableCell align="right">
                          {data.score?.toFixed(1)}%
                        </TableCell>
                        <TableCell align="right">
                          {data.weight?.toFixed(0)}%
                        </TableCell>
                        <TableCell align="center">
                          <Chip
                            label={data.status}
                            color={getStatusColor(data.status)}
                            size="small"
                          />
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            )}

            {/* Gaps */}
            {results.compliance.gaps && results.compliance.gaps.length > 0 && (
              <Box sx={{ mt: 3 }}>
                <Typography variant="subtitle1" gutterBottom>
                  Identified Gaps ({results.compliance.gaps.length})
                </Typography>
                {results.compliance.gaps.map((gap, index) => (
                  <Alert severity="warning" key={index} sx={{ mb: 1 }}>
                    <Typography variant="body2">
                      <strong>{gap.category?.replace(/_/g, ' ').toUpperCase()}:</strong> {gap.description}
                    </Typography>
                    {gap.recommendation && (
                      <Typography variant="caption" display="block" sx={{ mt: 0.5 }}>
                        💡 Recommendation: {gap.recommendation}
                      </Typography>
                    )}
                  </Alert>
                ))}
              </Box>
            )}
          </AccordionDetails>
        </Accordion>
      )}

      {/* Model-Specific Validation */}
      {results.model_specific && (
        <Accordion>
          <AccordionSummary expandIcon={<ExpandMore />}>
            <Typography variant="h6">🎯 Model-Specific Validation</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Typography variant="body2" paragraph>
              Model Type: <strong>{results.model_specific.model_type}</strong>
            </Typography>
            {results.model_specific.checks && (
              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Check</TableCell>
                      <TableCell>Result</TableCell>
                      <TableCell align="center">Status</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {Object.entries(results.model_specific.checks).map(([check, data]) => (
                      <TableRow key={check}>
                        <TableCell component="th" scope="row">
                          {check.replace(/_/g, ' ').toUpperCase()}
                        </TableCell>
                        <TableCell>
                          {typeof data === 'object' && data !== null ? (
                            <Box>
                              {data.train && <Typography variant="caption" display="block">Train: {data.train.status || 'OK'}</Typography>}
                              {data.test && <Typography variant="caption" display="block">Test: {data.test.status || 'OK'}</Typography>}
                              {data.oot && <Typography variant="caption" display="block">OOT: {data.oot.status || 'OK'}</Typography>}
                              {!data.train && !data.test && !data.oot && (
                                <Typography variant="caption">Check completed</Typography>
                              )}
                            </Box>
                          ) : (
                            String(data)
                          )}
                        </TableCell>
                        <TableCell align="center">
                          <Chip
                            label={data.status || 'passed'}
                            color={getStatusColor(data.status || 'passed')}
                            size="small"
                          />
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            )}
          </AccordionDetails>
        </Accordion>
      )}
    </Box>
  );
};

export default ValidationResults;

// Made with ❤️ by Bob

// Made with Bob
