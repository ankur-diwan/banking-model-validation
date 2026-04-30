import React, { useState } from 'react';
import { Outlet } from 'react-router-dom';
import { Box, CssBaseline, Toolbar } from '@mui/material';
import Sidebar from '../components/Navigation/Sidebar';
import TopBar from '../components/Navigation/TopBar';

const drawerWidth = 280;

const MainLayout = () => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const handleSidebarCollapse = () => {
    setSidebarCollapsed(!sidebarCollapsed);
  };

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh', bgcolor: 'background.default' }}>
      <CssBaseline />
      
      {/* Top Navigation Bar */}
      <TopBar 
        drawerWidth={sidebarCollapsed ? 70 : drawerWidth}
        onMenuClick={handleDrawerToggle}
        onSidebarCollapse={handleSidebarCollapse}
        sidebarCollapsed={sidebarCollapsed}
      />
      
      {/* Sidebar Navigation */}
      <Sidebar
        drawerWidth={drawerWidth}
        mobileOpen={mobileOpen}
        onDrawerToggle={handleDrawerToggle}
        collapsed={sidebarCollapsed}
      />
      
      {/* Main Content Area */}
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { 
            sm: `calc(100% - ${sidebarCollapsed ? 70 : drawerWidth}px)` 
          },
          ml: { 
            sm: `${sidebarCollapsed ? 70 : drawerWidth}px` 
          },
          transition: theme => theme.transitions.create(['margin', 'width'], {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.leavingScreen,
          }),
        }}
      >
        <Toolbar /> {/* Spacer for fixed AppBar */}
        <Outlet /> {/* Child routes render here */}
      </Box>
    </Box>
  );
};

export default MainLayout;

// Made with Bob
