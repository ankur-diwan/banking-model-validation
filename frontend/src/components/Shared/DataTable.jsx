import React, { useState, useMemo } from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  TableSortLabel,
  Paper,
  Checkbox,
  IconButton,
  Toolbar,
  Typography,
  Tooltip,
  TextField,
  InputAdornment,
  Box,
  Chip,
  Menu,
  MenuItem,
  Button
} from '@mui/material';
import {
  Search as SearchIcon,
  FilterList as FilterIcon,
  GetApp as ExportIcon,
  MoreVert as MoreIcon,
  Delete as DeleteIcon,
  Edit as EditIcon,
  Visibility as ViewIcon
} from '@mui/icons-material';

/**
 * Advanced reusable data table component with sorting, filtering, pagination, and bulk actions
 * 
 * @param {Object} props
 * @param {Array} props.columns - Column definitions [{ id, label, sortable, filterable, render }]
 * @param {Array} props.data - Table data
 * @param {Function} props.onRowClick - Row click handler
 * @param {Function} props.onBulkAction - Bulk action handler
 * @param {Array} props.bulkActions - Available bulk actions
 * @param {Boolean} props.selectable - Enable row selection
 * @param {Boolean} props.searchable - Enable search
 * @param {Boolean} props.exportable - Enable export
 * @param {String} props.title - Table title
 * @param {Number} props.defaultRowsPerPage - Default rows per page
 */
const DataTable = ({
  columns = [],
  data = [],
  onRowClick,
  onBulkAction,
  bulkActions = [],
  selectable = false,
  searchable = true,
  exportable = true,
  title = '',
  defaultRowsPerPage = 10,
  rowActions = []
}) => {
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(defaultRowsPerPage);
  const [orderBy, setOrderBy] = useState('');
  const [order, setOrder] = useState('asc');
  const [selected, setSelected] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterAnchorEl, setFilterAnchorEl] = useState(null);
  const [rowActionAnchorEl, setRowActionAnchorEl] = useState(null);
  const [activeRowId, setActiveRowId] = useState(null);

  // Handle sorting
  const handleSort = (columnId) => {
    const isAsc = orderBy === columnId && order === 'asc';
    setOrder(isAsc ? 'desc' : 'asc');
    setOrderBy(columnId);
  };

  // Handle selection
  const handleSelectAll = (event) => {
    if (event.target.checked) {
      const newSelected = filteredData.map((row) => row.id);
      setSelected(newSelected);
    } else {
      setSelected([]);
    }
  };

  const handleSelectRow = (event, id) => {
    event.stopPropagation();
    const selectedIndex = selected.indexOf(id);
    let newSelected = [];

    if (selectedIndex === -1) {
      newSelected = newSelected.concat(selected, id);
    } else if (selectedIndex === 0) {
      newSelected = newSelected.concat(selected.slice(1));
    } else if (selectedIndex === selected.length - 1) {
      newSelected = newSelected.concat(selected.slice(0, -1));
    } else if (selectedIndex > 0) {
      newSelected = newSelected.concat(
        selected.slice(0, selectedIndex),
        selected.slice(selectedIndex + 1)
      );
    }

    setSelected(newSelected);
  };

  // Filter data based on search term
  const filteredData = useMemo(() => {
    if (!searchTerm) return data;

    return data.filter((row) =>
      columns.some((column) => {
        const value = row[column.id];
        if (value === null || value === undefined) return false;
        return String(value).toLowerCase().includes(searchTerm.toLowerCase());
      })
    );
  }, [data, searchTerm, columns]);

  // Sort data
  const sortedData = useMemo(() => {
    if (!orderBy) return filteredData;

    return [...filteredData].sort((a, b) => {
      const aValue = a[orderBy];
      const bValue = b[orderBy];

      if (aValue === null || aValue === undefined) return 1;
      if (bValue === null || bValue === undefined) return -1;

      if (typeof aValue === 'string') {
        return order === 'asc'
          ? aValue.localeCompare(bValue)
          : bValue.localeCompare(aValue);
      }

      return order === 'asc' ? aValue - bValue : bValue - aValue;
    });
  }, [filteredData, orderBy, order]);

  // Paginate data
  const paginatedData = useMemo(() => {
    const startIndex = page * rowsPerPage;
    return sortedData.slice(startIndex, startIndex + rowsPerPage);
  }, [sortedData, page, rowsPerPage]);

  // Handle pagination
  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  // Handle export
  const handleExport = () => {
    const csvContent = [
      columns.map((col) => col.label).join(','),
      ...sortedData.map((row) =>
        columns.map((col) => {
          const value = row[col.id];
          return typeof value === 'string' && value.includes(',')
            ? `"${value}"`
            : value;
        }).join(',')
      )
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${title || 'data'}_${new Date().toISOString()}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
  };

  // Handle bulk actions
  const handleBulkAction = (action) => {
    if (onBulkAction) {
      onBulkAction(action, selected);
    }
    setSelected([]);
  };

  // Handle row actions
  const handleRowAction = (action, rowId) => {
    if (action.onClick) {
      action.onClick(rowId);
    }
    setRowActionAnchorEl(null);
    setActiveRowId(null);
  };

  const isSelected = (id) => selected.indexOf(id) !== -1;

  return (
    <Paper sx={{ width: '100%', mb: 2 }}>
      {/* Toolbar */}
      <Toolbar
        sx={{
          pl: { sm: 2 },
          pr: { xs: 1, sm: 1 },
          ...(selected.length > 0 && {
            bgcolor: (theme) =>
              theme.palette.mode === 'light'
                ? theme.palette.primary.light
                : theme.palette.primary.dark,
          }),
        }}
      >
        {selected.length > 0 ? (
          <Typography
            sx={{ flex: '1 1 100%' }}
            color="inherit"
            variant="subtitle1"
            component="div"
          >
            {selected.length} selected
          </Typography>
        ) : (
          <Typography
            sx={{ flex: '1 1 100%' }}
            variant="h6"
            id="tableTitle"
            component="div"
          >
            {title}
          </Typography>
        )}

        {selected.length > 0 ? (
          <Box sx={{ display: 'flex', gap: 1 }}>
            {bulkActions.map((action) => (
              <Tooltip key={action.id} title={action.label}>
                <IconButton onClick={() => handleBulkAction(action.id)}>
                  {action.icon}
                </IconButton>
              </Tooltip>
            ))}
          </Box>
        ) : (
          <Box sx={{ display: 'flex', gap: 1 }}>
            {searchable && (
              <TextField
                size="small"
                placeholder="Search..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <SearchIcon />
                    </InputAdornment>
                  ),
                }}
              />
            )}
            {exportable && (
              <Tooltip title="Export">
                <IconButton onClick={handleExport}>
                  <ExportIcon />
                </IconButton>
              </Tooltip>
            )}
          </Box>
        )}
      </Toolbar>

      {/* Table */}
      <TableContainer>
        <Table sx={{ minWidth: 750 }} size="medium">
          <TableHead>
            <TableRow>
              {selectable && (
                <TableCell padding="checkbox">
                  <Checkbox
                    color="primary"
                    indeterminate={
                      selected.length > 0 && selected.length < filteredData.length
                    }
                    checked={
                      filteredData.length > 0 &&
                      selected.length === filteredData.length
                    }
                    onChange={handleSelectAll}
                  />
                </TableCell>
              )}
              {columns.map((column) => (
                <TableCell
                  key={column.id}
                  sortDirection={orderBy === column.id ? order : false}
                >
                  {column.sortable !== false ? (
                    <TableSortLabel
                      active={orderBy === column.id}
                      direction={orderBy === column.id ? order : 'asc'}
                      onClick={() => handleSort(column.id)}
                    >
                      {column.label}
                    </TableSortLabel>
                  ) : (
                    column.label
                  )}
                </TableCell>
              ))}
              {rowActions.length > 0 && (
                <TableCell align="right">Actions</TableCell>
              )}
            </TableRow>
          </TableHead>
          <TableBody>
            {paginatedData.map((row) => {
              const isItemSelected = isSelected(row.id);

              return (
                <TableRow
                  hover
                  onClick={() => onRowClick && onRowClick(row)}
                  role="checkbox"
                  aria-checked={isItemSelected}
                  tabIndex={-1}
                  key={row.id}
                  selected={isItemSelected}
                  sx={{ cursor: onRowClick ? 'pointer' : 'default' }}
                >
                  {selectable && (
                    <TableCell padding="checkbox">
                      <Checkbox
                        color="primary"
                        checked={isItemSelected}
                        onClick={(event) => handleSelectRow(event, row.id)}
                      />
                    </TableCell>
                  )}
                  {columns.map((column) => (
                    <TableCell key={column.id}>
                      {column.render
                        ? column.render(row[column.id], row)
                        : row[column.id]}
                    </TableCell>
                  ))}
                  {rowActions.length > 0 && (
                    <TableCell align="right">
                      <IconButton
                        size="small"
                        onClick={(e) => {
                          e.stopPropagation();
                          setRowActionAnchorEl(e.currentTarget);
                          setActiveRowId(row.id);
                        }}
                      >
                        <MoreIcon />
                      </IconButton>
                    </TableCell>
                  )}
                </TableRow>
              );
            })}
            {paginatedData.length === 0 && (
              <TableRow>
                <TableCell
                  colSpan={
                    columns.length +
                    (selectable ? 1 : 0) +
                    (rowActions.length > 0 ? 1 : 0)
                  }
                  align="center"
                >
                  <Typography variant="body2" color="text.secondary">
                    No data available
                  </Typography>
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Pagination */}
      <TablePagination
        rowsPerPageOptions={[5, 10, 25, 50]}
        component="div"
        count={sortedData.length}
        rowsPerPage={rowsPerPage}
        page={page}
        onPageChange={handleChangePage}
        onRowsPerPageChange={handleChangeRowsPerPage}
      />

      {/* Row Actions Menu */}
      <Menu
        anchorEl={rowActionAnchorEl}
        open={Boolean(rowActionAnchorEl)}
        onClose={() => {
          setRowActionAnchorEl(null);
          setActiveRowId(null);
        }}
      >
        {rowActions.map((action) => (
          <MenuItem
            key={action.id}
            onClick={() => handleRowAction(action, activeRowId)}
          >
            {action.icon && <Box sx={{ mr: 1 }}>{action.icon}</Box>}
            {action.label}
          </MenuItem>
        ))}
      </Menu>
    </Paper>
  );
};

export default DataTable;

// Made with Bob
