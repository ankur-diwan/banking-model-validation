import React from 'react';
import { createBrowserRouter, Navigate } from 'react-router-dom';
import MainLayout from '../layouts/MainLayout';
import AuthLayout from '../layouts/AuthLayout';

// Pages - will be created
import DashboardPage from '../pages/DashboardPage';
import ValidationWizardPage from '../pages/ValidationWizardPage';
import ValidationHistoryPage from '../pages/ValidationHistoryPage';
import TestSelectionPage from '../pages/TestSelectionPage';
import ModelInventoryPage from '../pages/ModelInventoryPage';
import ModelOnboardingPage from '../pages/ModelOnboardingPage';
import ModelVersionsPage from '../pages/ModelVersionsPage';
import MonitoringDashboardPage from '../pages/MonitoringDashboardPage';
import PerformanceMetricsPage from '../pages/PerformanceMetricsPage';
import DriftDetectionPage from '../pages/DriftDetectionPage';
import AlertsPage from '../pages/AlertsPage';
import ComplianceDashboardPage from '../pages/ComplianceDashboardPage';
import ModelCardsPage from '../pages/ModelCardsPage';
import AuditTrailPage from '../pages/AuditTrailPage';
import ComplianceReportsPage from '../pages/ComplianceReportsPage';
import WorkflowsPage from '../pages/WorkflowsPage';
import TaskInboxPage from '../pages/TaskInboxPage';
import ApprovalsPage from '../pages/ApprovalsPage';
import CustomTestsPage from '../pages/CustomTestsPage';
import CreateTestPage from '../pages/CreateTestPage';
import ExecuteTestsPage from '../pages/ExecuteTestsPage';
import StressTestingPage from '../pages/StressTestingPage';
import StressTestConfigPage from '../pages/StressTestConfigPage';
import StressTestResultsPage from '../pages/StressTestResultsPage';
import DocumentationPage from '../pages/DocumentationPage';
import RAGAssistantPage from '../pages/RAGAssistantPage';
import DocumentEditorPage from '../pages/DocumentEditorPage';
import HelpCenterPage from '../pages/HelpCenterPage';
import LoginPage from '../pages/LoginPage';
import ProfilePage from '../pages/ProfilePage';
import SettingsPage from '../pages/SettingsPage';
import NotFoundPage from '../pages/NotFoundPage';

const router = createBrowserRouter([
  {
    path: '/',
    element: <MainLayout />,
    children: [
      {
        index: true,
        element: <Navigate to="/dashboard" replace />,
      },
      {
        path: 'dashboard',
        element: <DashboardPage />,
      },
      // Validation Routes
      {
        path: 'validation',
        children: [
          {
            index: true,
            element: <Navigate to="/validation/new" replace />,
          },
          {
            path: 'new',
            element: <ValidationWizardPage />,
          },
          {
            path: 'history',
            element: <ValidationHistoryPage />,
          },
          {
            path: 'tests',
            element: <TestSelectionPage />,
          },
        ],
      },
      // Model Inventory Routes
      {
        path: 'models',
        children: [
          {
            index: true,
            element: <ModelInventoryPage />,
          },
          {
            path: 'onboard',
            element: <ModelOnboardingPage />,
          },
          {
            path: 'versions',
            element: <ModelVersionsPage />,
          },
        ],
      },
      // Monitoring Routes
      {
        path: 'monitoring',
        children: [
          {
            index: true,
            element: <MonitoringDashboardPage />,
          },
          {
            path: 'performance',
            element: <PerformanceMetricsPage />,
          },
          {
            path: 'drift',
            element: <DriftDetectionPage />,
          },
          {
            path: 'alerts',
            element: <AlertsPage />,
          },
        ],
      },
      // Compliance Routes
      {
        path: 'compliance',
        children: [
          {
            index: true,
            element: <ComplianceDashboardPage />,
          },
          {
            path: 'model-cards',
            element: <ModelCardsPage />,
          },
          {
            path: 'audit',
            element: <AuditTrailPage />,
          },
          {
            path: 'reports',
            element: <ComplianceReportsPage />,
          },
        ],
      },
      // Workflow Routes
      {
        path: 'workflows',
        children: [
          {
            index: true,
            element: <WorkflowsPage />,
          },
          {
            path: 'tasks',
            element: <TaskInboxPage />,
          },
          {
            path: 'approvals',
            element: <ApprovalsPage />,
          },
        ],
      },
      // Custom Tests Routes
      {
        path: 'custom-tests',
        children: [
          {
            index: true,
            element: <CustomTestsPage />,
          },
          {
            path: 'create',
            element: <CreateTestPage />,
          },
          {
            path: 'execute',
            element: <ExecuteTestsPage />,
          },
        ],
      },
      // Stress Testing Routes
      {
        path: 'stress-testing',
        children: [
          {
            index: true,
            element: <StressTestingPage />,
          },
          {
            path: 'config',
            element: <StressTestConfigPage />,
          },
          {
            path: 'results',
            element: <StressTestResultsPage />,
          },
        ],
      },
      // Documentation Routes
      {
        path: 'documentation',
        children: [
          {
            index: true,
            element: <DocumentationPage />,
          },
          {
            path: 'rag',
            element: <RAGAssistantPage />,
          },
          {
            path: 'editor',
            element: <DocumentEditorPage />,
          },
        ],
      },
      // Other Routes
      {
        path: 'help',
        element: <HelpCenterPage />,
      },
      {
        path: 'profile',
        element: <ProfilePage />,
      },
      {
        path: 'settings',
        element: <SettingsPage />,
      },
    ],
  },
  // Auth Routes
  {
    path: '/auth',
    element: <AuthLayout />,
    children: [
      {
        path: 'login',
        element: <LoginPage />,
      },
    ],
  },
  // Redirect /login to /auth/login
  {
    path: '/login',
    element: <Navigate to="/auth/login" replace />,
  },
  // 404 Not Found
  {
    path: '*',
    element: <NotFoundPage />,
  },
]);

export default router;

// Made with Bob
