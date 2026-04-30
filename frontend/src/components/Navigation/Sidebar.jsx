import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  Box,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Divider,
  Toolbar,
  Typography,
  Collapse,
  Tooltip,
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  Assessment as AssessmentIcon,
  Inventory as InventoryIcon,
  MonitorHeart as MonitorIcon,
  Gavel as ComplianceIcon,
  AccountTree as WorkflowIcon,
  Science as TestIcon,
  TrendingUp as StressTestIcon,
  MenuBook as DocumentIcon,
  Help as HelpIcon,
  ExpandLess,
  ExpandMore,
  AccountBalance as BankIcon,
} from '@mui/icons-material';

const Sidebar = ({ drawerWidth, mobileOpen, onDrawerToggle, collapsed }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const [openMenus, setOpenMenus] = React.useState({});

  const handleMenuClick = (path, hasSubmenu, menuKey) => {
    if (hasSubmenu) {
      setOpenMenus(prev => ({
        ...prev,
        [menuKey]: !prev[menuKey]
      }));
    } else {
      navigate(path);
      if (mobileOpen) {
        onDrawerToggle();
      }
    }
  };

  const isActive = (path) => location.pathname === path;

  const menuItems = [
    {
      title: 'Dashboard',
      icon: <DashboardIcon />,
      path: '/dashboard',
    },
    {
      title: 'Model Validation',
      icon: <AssessmentIcon />,
      path: '/validation',
      submenu: [
        { title: 'New Validation', path: '/validation/new' },
        { title: 'Validation History', path: '/validation/history' },
        { title: 'Test Selection', path: '/validation/tests' },
      ],
    },
    {
      title: 'Model Inventory',
      icon: <InventoryIcon />,
      path: '/models',
      submenu: [
        { title: 'All Models', path: '/models' },
        { title: 'Onboard Model', path: '/models/onboard' },
        { title: 'Model Versions', path: '/models/versions' },
      ],
    },
    {
      title: 'Monitoring',
      icon: <MonitorIcon />,
      path: '/monitoring',
      submenu: [
        { title: 'Overview', path: '/monitoring' },
        { title: 'Performance Metrics', path: '/monitoring/performance' },
        { title: 'Drift Detection', path: '/monitoring/drift' },
        { title: 'Alerts', path: '/monitoring/alerts' },
      ],
    },
    {
      title: 'Compliance',
      icon: <ComplianceIcon />,
      path: '/compliance',
      submenu: [
        { title: 'Dashboard', path: '/compliance' },
        { title: 'Model Cards', path: '/compliance/model-cards' },
        { title: 'Audit Trail', path: '/compliance/audit' },
        { title: 'Reports', path: '/compliance/reports' },
      ],
    },
    {
      title: 'Workflows',
      icon: <WorkflowIcon />,
      path: '/workflows',
      submenu: [
        { title: 'Active Workflows', path: '/workflows' },
        { title: 'Task Inbox', path: '/workflows/tasks' },
        { title: 'Approvals', path: '/workflows/approvals' },
      ],
    },
    {
      title: 'Custom Tests',
      icon: <TestIcon />,
      path: '/custom-tests',
      submenu: [
        { title: 'Test Library', path: '/custom-tests' },
        { title: 'Create Test', path: '/custom-tests/create' },
        { title: 'Execute Tests', path: '/custom-tests/execute' },
      ],
    },
    {
      title: 'Stress Testing',
      icon: <StressTestIcon />,
      path: '/stress-testing',
      submenu: [
        { title: 'Scenarios', path: '/stress-testing' },
        { title: 'Configure Test', path: '/stress-testing/config' },
        { title: 'Results', path: '/stress-testing/results' },
      ],
    },
    {
      title: 'Documentation',
      icon: <DocumentIcon />,
      path: '/documentation',
      submenu: [
        { title: 'Document Viewer', path: '/documentation' },
        { title: 'RAG Assistant', path: '/documentation/rag' },
        { title: 'Editor', path: '/documentation/editor' },
      ],
    },
  ];

  const bottomMenuItems = [
    {
      title: 'Help Center',
      icon: <HelpIcon />,
      path: '/help',
    },
  ];

  const renderMenuItem = (item, index) => {
    const hasSubmenu = item.submenu && item.submenu.length > 0;
    const isMenuOpen = openMenus[item.title];
    const isItemActive = isActive(item.path);

    return (
      <React.Fragment key={index}>
        <ListItem disablePadding sx={{ display: 'block' }}>
          <Tooltip title={collapsed ? item.title : ''} placement="right">
            <ListItemButton
              onClick={() => handleMenuClick(item.path, hasSubmenu, item.title)}
              sx={{
                minHeight: 48,
                justifyContent: collapsed ? 'center' : 'initial',
                px: 2.5,
                bgcolor: isItemActive ? 'action.selected' : 'transparent',
                '&:hover': {
                  bgcolor: 'action.hover',
                },
              }}
            >
              <ListItemIcon
                sx={{
                  minWidth: 0,
                  mr: collapsed ? 0 : 3,
                  justifyContent: 'center',
                  color: isItemActive ? 'primary.main' : 'inherit',
                }}
              >
                {item.icon}
              </ListItemIcon>
              {!collapsed && (
                <>
                  <ListItemText 
                    primary={item.title}
                    sx={{
                      color: isItemActive ? 'primary.main' : 'inherit',
                    }}
                  />
                  {hasSubmenu && (isMenuOpen ? <ExpandLess /> : <ExpandMore />)}
                </>
              )}
            </ListItemButton>
          </Tooltip>
        </ListItem>
        
        {hasSubmenu && !collapsed && (
          <Collapse in={isMenuOpen} timeout="auto" unmountOnExit>
            <List component="div" disablePadding>
              {item.submenu.map((subItem, subIndex) => (
                <ListItemButton
                  key={subIndex}
                  onClick={() => handleMenuClick(subItem.path, false)}
                  sx={{
                    pl: 4,
                    bgcolor: isActive(subItem.path) ? 'action.selected' : 'transparent',
                  }}
                >
                  <ListItemText 
                    primary={subItem.title}
                    sx={{
                      color: isActive(subItem.path) ? 'primary.main' : 'inherit',
                    }}
                  />
                </ListItemButton>
              ))}
            </List>
          </Collapse>
        )}
      </React.Fragment>
    );
  };

  const drawerContent = (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <Toolbar>
        {!collapsed && (
          <Box sx={{ display: 'flex', alignItems: 'center', width: '100%' }}>
            <BankIcon sx={{ mr: 1, color: 'primary.main' }} />
            <Box>
              <Typography variant="h6" noWrap component="div" fontWeight="bold">
                Model Validation
              </Typography>
              <Typography variant="caption" color="text.secondary">
                Banking System
              </Typography>
            </Box>
          </Box>
        )}
        {collapsed && (
          <BankIcon sx={{ color: 'primary.main' }} />
        )}
      </Toolbar>
      
      <Divider />
      
      <Box sx={{ flexGrow: 1, overflow: 'auto' }}>
        <List>
          {menuItems.map((item, index) => renderMenuItem(item, index))}
        </List>
      </Box>
      
      <Divider />
      
      <List>
        {bottomMenuItems.map((item, index) => renderMenuItem(item, index))}
      </List>
    </Box>
  );

  return (
    <Box
      component="nav"
      sx={{ 
        width: { sm: collapsed ? 70 : drawerWidth }, 
        flexShrink: { sm: 0 } 
      }}
    >
      {/* Mobile drawer */}
      <Drawer
        variant="temporary"
        open={mobileOpen}
        onClose={onDrawerToggle}
        ModalProps={{
          keepMounted: true, // Better mobile performance
        }}
        sx={{
          display: { xs: 'block', sm: 'none' },
          '& .MuiDrawer-paper': {
            boxSizing: 'border-box',
            width: drawerWidth,
          },
        }}
      >
        {drawerContent}
      </Drawer>

      {/* Desktop drawer */}
      <Drawer
        variant="permanent"
        sx={{
          display: { xs: 'none', sm: 'block' },
          '& .MuiDrawer-paper': {
            boxSizing: 'border-box',
            width: collapsed ? 70 : drawerWidth,
            transition: theme => theme.transitions.create('width', {
              easing: theme.transitions.easing.sharp,
              duration: theme.transitions.duration.enteringScreen,
            }),
          },
        }}
        open
      >
        {drawerContent}
      </Drawer>
    </Box>
  );
};

export default Sidebar;

// Made with Bob
