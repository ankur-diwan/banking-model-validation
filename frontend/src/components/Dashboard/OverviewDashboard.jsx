/**
 * Overview Dashboard Component
 * Main dashboard showing key metrics and KPIs
 */

import React, { useEffect, useState } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  CircularProgress,
  Alert,
  Chip,
  LinearProgress,
} from '@mui/material';
import {
  TrendingUp,
  Assessment,
  CheckCircle,
  Warning,
  Error as ErrorIcon,
  Speed,
} from '@mui/icons-material';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { governanceAPI, mlopsAPI } from '../../services/api';
import useStore from '../../store/useStore';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

const MetricCard = ({ title, value, change, icon: Icon, color = 'primary' }) => (
  <Card>
    <CardContent>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <Box>
          <Typography color="text.secondary" gutterBottom variant="body2">
            {title}
          </Typography>
          <Typography variant="h4" component="div">
            {value}
          </Typography>
          {change && (
            <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
              <TrendingUp fontSize="small" color={change > 0 ? 'success' : 'error'} />
              <Typography
                variant="body2"
                color={change > 0 ? 'success.main' : 'error.main'}
                sx={{ ml: 0.5 }}
              >
                {change > 0 ? '+' : ''}{change}%
              </Typography>
            </Box>
          )}
        </Box>
        <Box
          sx={{
            backgroundColor: `${color}.light`,
            borderRadius: 2,
            p: 1,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <Icon color={color} />
        </Box>
      </Box>
    </CardContent>
  </Card>
);

const OverviewDashboard = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [metrics, setMetrics] = useState({
    totalModels: 0,
    activeModels: 0,
    validationsThisMonth: 0,
    complianceRate: 0,
  });
  const [modelsByType, setModelsByType] = useState([]);
  const [modelsByStatus, setModelsByStatus] = useState([]);
  const [performanceTrend, setPerformanceTrend] = useState([]);
  const [recentActivity, setRecentActivity] = useState([]);

  const { models, setModels, dashboardFilters } = useStore();

  useEffect(() => {
    fetchDashboardData();
  }, [dashboardFilters]);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Fetch models
      const modelsResponse = await governanceAPI.listModels();
      const modelsData = modelsResponse.data.models || [];
      setModels(modelsData);

      // Calculate metrics
      const totalModels = modelsData.length;
      const activeModels = modelsData.filter(
        (m) => m.lifecycle_stage === 'deployed' || m.lifecycle_stage === 'monitoring'
      ).length;

      setMetrics({
        totalModels,
        activeModels,
        validationsThisMonth: Math.floor(totalModels * 0.3), // Simulated
        complianceRate: 95, // Simulated
      });

      // Group by model type
      const typeGroups = modelsData.reduce((acc, model) => {
        const type = model.model_type || 'Unknown';
        acc[type] = (acc[type] || 0) + 1;
        return acc;
      }, {});

      setModelsByType(
        Object.entries(typeGroups).map(([name, value]) => ({ name, value }))
      );

      // Group by status
      const statusGroups = modelsData.reduce((acc, model) => {
        const status = model.lifecycle_stage || 'Unknown';
        acc[status] = (acc[status] || 0) + 1;
        return acc;
      }, {});

      setModelsByStatus(
        Object.entries(statusGroups).map(([name, value]) => ({ name, value }))
      );

      // Generate performance trend (simulated)
      setPerformanceTrend([
        { month: 'Jan', auc: 0.72, ks: 0.32 },
        { month: 'Feb', auc: 0.74, ks: 0.34 },
        { month: 'Mar', auc: 0.75, ks: 0.35 },
        { month: 'Apr', auc: 0.76, ks: 0.36 },
        { month: 'May', auc: 0.75, ks: 0.35 },
        { month: 'Jun', auc: 0.77, ks: 0.37 },
      ]);

      // Recent activity (simulated)
      setRecentActivity([
        { id: 1, type: 'validation', model: 'Model_A', status: 'completed', time: '2 hours ago' },
        { id: 2, type: 'deployment', model: 'Model_B', status: 'in_progress', time: '4 hours ago' },
        { id: 3, type: 'monitoring', model: 'Model_C', status: 'alert', time: '6 hours ago' },
      ]);

    } catch (err) {
      console.error('Failed to fetch dashboard data:', err);
      setError('Failed to load dashboard data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: 400 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mb: 3 }}>
        {error}
      </Alert>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dashboard Overview
      </Typography>
      <Typography variant="body2" color="text.secondary" paragraph>
        Key metrics and insights for model validation and governance
      </Typography>

      {/* Key Metrics */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Total Models"
            value={metrics.totalModels}
            change={12}
            icon={Assessment}
            color="primary"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Active Models"
            value={metrics.activeModels}
            change={8}
            icon={CheckCircle}
            color="success"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Validations (MTD)"
            value={metrics.validationsThisMonth}
            change={-5}
            icon={Speed}
            color="info"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Compliance Rate"
            value={`${metrics.complianceRate}%`}
            change={2}
            icon={CheckCircle}
            color="success"
          />
        </Grid>
      </Grid>

      {/* Charts */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        {/* Performance Trend */}
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Performance Trend
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={performanceTrend}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="auc" stroke="#8884d8" name="AUC" />
                  <Line type="monotone" dataKey="ks" stroke="#82ca9d" name="KS" />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Models by Status */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Models by Status
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={modelsByStatus}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {modelsByStatus.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Models by Type */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Models by Type
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={modelsByType}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="value" fill="#8884d8" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Recent Activity */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Recent Activity
              </Typography>
              <Box>
                {recentActivity.map((activity) => (
                  <Box
                    key={activity.id}
                    sx={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      py: 1.5,
                      borderBottom: '1px solid',
                      borderColor: 'divider',
                      '&:last-child': { borderBottom: 'none' },
                    }}
                  >
                    <Box>
                      <Typography variant="body2" fontWeight="medium">
                        {activity.model}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        {activity.type} • {activity.time}
                      </Typography>
                    </Box>
                    <Chip
                      label={activity.status}
                      size="small"
                      color={
                        activity.status === 'completed'
                          ? 'success'
                          : activity.status === 'alert'
                          ? 'error'
                          : 'warning'
                      }
                    />
                  </Box>
                ))}
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Alerts */}
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            System Alerts
          </Typography>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
            <Alert severity="warning" icon={<Warning />}>
              Model_XYZ showing performance degradation. Review recommended.
            </Alert>
            <Alert severity="info">
              3 models pending validation approval.
            </Alert>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};

export default OverviewDashboard;

// Made with ❤️ by Bob

// Made with Bob
