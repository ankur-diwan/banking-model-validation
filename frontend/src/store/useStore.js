/**
 * Zustand Store for Banking Model Validation System
 * Centralized state management
 */

import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

const useStore = create(
  devtools(
    persist(
      (set, get) => ({
        // ==================== User State ====================
        user: null,
        setUser: (user) => set({ user }),
        
        // ==================== Model Configuration ====================
        currentModelConfig: {
          model_name: '',
          product_type: '',
          scorecard_type: '',
          model_type: '',
          description: '',
          version: '1.0',
          owner: 'Model Risk Management',
          features: [],
          data_version: '1.0',
        },
        setModelConfig: (config) => set({ currentModelConfig: config }),
        updateModelConfig: (updates) => 
          set((state) => ({
            currentModelConfig: { ...state.currentModelConfig, ...updates }
          })),
        resetModelConfig: () => 
          set({
            currentModelConfig: {
              model_name: '',
              product_type: '',
              scorecard_type: '',
              model_type: '',
              description: '',
              version: '1.0',
              owner: 'Model Risk Management',
              features: [],
              data_version: '1.0',
            }
          }),
        
        // ==================== Use Cases ====================
        useCases: [],
        setUseCases: (useCases) => set({ useCases }),
        addUseCase: (useCase) => 
          set((state) => ({ useCases: [...state.useCases, useCase] })),
        
        // ==================== Models ====================
        models: [],
        setModels: (models) => set({ models }),
        addModel: (model) => 
          set((state) => ({ models: [...state.models, model] })),
        updateModel: (modelId, updates) => 
          set((state) => ({
            models: state.models.map((m) => 
              m.model_id === modelId ? { ...m, ...updates } : m
            )
          })),
        
        // ==================== Selected Model ====================
        selectedModel: null,
        setSelectedModel: (model) => set({ selectedModel: model }),
        
        // ==================== Model Versions ====================
        modelVersions: {},
        setModelVersions: (modelId, versions) => 
          set((state) => ({
            modelVersions: { ...state.modelVersions, [modelId]: versions }
          })),
        
        // ==================== Monitoring Data ====================
        monitoringData: {},
        setMonitoringData: (modelId, versionId, data) => 
          set((state) => ({
            monitoringData: {
              ...state.monitoringData,
              [`${modelId}_${versionId}`]: data
            }
          })),
        
        // ==================== Workflows ====================
        workflows: [],
        setWorkflows: (workflows) => set({ workflows }),
        addWorkflow: (workflow) => 
          set((state) => ({ workflows: [...state.workflows, workflow] })),
        updateWorkflow: (workflowId, updates) => 
          set((state) => ({
            workflows: state.workflows.map((w) => 
              w.workflow_id === workflowId ? { ...w, ...updates } : w
            )
          })),
        
        // ==================== Tasks ====================
        tasks: [],
        setTasks: (tasks) => set({ tasks }),
        addTask: (task) => 
          set((state) => ({ tasks: [...state.tasks, task] })),
        updateTask: (taskId, updates) => 
          set((state) => ({
            tasks: state.tasks.map((t) => 
              t.task_id === taskId ? { ...t, ...updates } : t
            )
          })),
        
        // ==================== Validation State ====================
        validations: [],
        setValidations: (validations) => set({ validations }),
        addValidation: (validation) => 
          set((state) => ({ validations: [...state.validations, validation] })),
        updateValidation: (validationId, updates) => 
          set((state) => ({
            validations: state.validations.map((v) => 
              v.validation_id === validationId ? { ...v, ...updates } : v
            )
          })),
        
        // ==================== Stress Tests ====================
        stressTests: [],
        setStressTests: (tests) => set({ stressTests: tests }),
        addStressTest: (test) => 
          set((state) => ({ stressTests: [...state.stressTests, test] })),
        updateStressTest: (testId, updates) => 
          set((state) => ({
            stressTests: state.stressTests.map((t) => 
              t.test_id === testId ? { ...t, ...updates } : t
            )
          })),
        
        // ==================== Custom Tests ====================
        customTests: [],
        setCustomTests: (tests) => set({ customTests: tests }),
        addCustomTest: (test) => 
          set((state) => ({ customTests: [...state.customTests, test] })),
        updateCustomTest: (testId, updates) => 
          set((state) => ({
            customTests: state.customTests.map((t) => 
              t.test_id === testId ? { ...t, ...updates } : t
            )
          })),
        
        // ==================== UI State ====================
        activeTab: 'dashboard',
        setActiveTab: (tab) => set({ activeTab: tab }),
        
        sidebarOpen: true,
        setSidebarOpen: (open) => set({ sidebarOpen: open }),
        
        loading: {
          models: false,
          validation: false,
          deployment: false,
          monitoring: false,
        },
        setLoading: (key, value) => 
          set((state) => ({
            loading: { ...state.loading, [key]: value }
          })),
        
        // ==================== Notifications ====================
        notifications: [],
        addNotification: (notification) => 
          set((state) => ({
            notifications: [...state.notifications, {
              id: Date.now(),
              timestamp: new Date().toISOString(),
              ...notification
            }]
          })),
        removeNotification: (id) => 
          set((state) => ({
            notifications: state.notifications.filter((n) => n.id !== id)
          })),
        clearNotifications: () => set({ notifications: [] }),
        
        // ==================== WebSocket State ====================
        wsConnected: false,
        setWsConnected: (connected) => set({ wsConnected: connected }),
        
        // ==================== Dashboard Filters ====================
        dashboardFilters: {
          dateRange: 'last_30_days',
          productType: 'all',
          scorecardType: 'all',
          modelType: 'all',
          status: 'all',
        },
        setDashboardFilters: (filters) => 
          set((state) => ({
            dashboardFilters: { ...state.dashboardFilters, ...filters }
          })),
        
        // ==================== Model Recommendations ====================
        modelRecommendations: null,
        setModelRecommendations: (recommendations) => 
          set({ modelRecommendations: recommendations }),
        
        // ==================== Compliance Data ====================
        complianceReports: {},
        setComplianceReport: (modelId, report) => 
          set((state) => ({
            complianceReports: { ...state.complianceReports, [modelId]: report }
          })),
        
        // ==================== Model Cards ====================
        modelCards: {},
        setModelCard: (modelId, card) => 
          set((state) => ({
            modelCards: { ...state.modelCards, [modelId]: card }
          })),
        
        // ==================== Performance Metrics ====================
        performanceMetrics: {},
        setPerformanceMetrics: (modelId, versionId, metrics) => 
          set((state) => ({
            performanceMetrics: {
              ...state.performanceMetrics,
              [`${modelId}_${versionId}`]: metrics
            }
          })),
        
        // ==================== Alerts ====================
        alerts: [],
        addAlert: (alert) => 
          set((state) => ({
            alerts: [...state.alerts, {
              id: Date.now(),
              timestamp: new Date().toISOString(),
              ...alert
            }]
          })),
        removeAlert: (id) => 
          set((state) => ({
            alerts: state.alerts.filter((a) => a.id !== id)
          })),
        clearAlerts: () => set({ alerts: [] }),
        
        // ==================== Actions ====================
        
        // Reset all data (for logout)
        resetStore: () => 
          set({
            user: null,
            useCases: [],
            models: [],
            selectedModel: null,
            modelVersions: {},
            monitoringData: {},
            workflows: [],
            tasks: [],
            validations: [],
            stressTests: [],
            customTests: [],
            notifications: [],
            alerts: [],
            complianceReports: {},
            modelCards: {},
            performanceMetrics: {},
            modelRecommendations: null,
          }),
        
        // Bulk update for real-time data
        bulkUpdate: (updates) => set((state) => ({ ...state, ...updates })),
        
      }),
      {
        name: 'banking-validation-store',
        partialize: (state) => ({
          // Only persist certain parts of the state
          user: state.user,
          currentModelConfig: state.currentModelConfig,
          dashboardFilters: state.dashboardFilters,
          activeTab: state.activeTab,
          sidebarOpen: state.sidebarOpen,
        }),
      }
    ),
    {
      name: 'banking-validation-store',
    }
  )
);

export default useStore;

// Made with ❤️ by Bob

// Made with Bob
