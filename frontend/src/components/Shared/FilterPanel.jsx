import React, { useState } from 'react';
import {
  Paper,
  Box,
  Typography,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Chip,
  Button,
  IconButton,
  Collapse,
  Divider,
  Slider,
  FormControlLabel,
  Checkbox,
  Radio,
  RadioGroup,
  Autocomplete
} from '@mui/material';
import {
  FilterList as FilterIcon,
  Clear as ClearIcon,
  ExpandMore as ExpandIcon,
  ExpandLess as CollapseIcon
} from '@mui/icons-material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';

/**
 * Reusable filter panel component with various filter types
 * 
 * @param {Object} props
 * @param {Array} props.filters - Filter definitions
 * @param {Object} props.values - Current filter values
 * @param {Function} props.onChange - Change handler
 * @param {Function} props.onApply - Apply handler
 * @param {Function} props.onClear - Clear handler
 * @param {Boolean} props.collapsible - Enable collapse
 * @param {Boolean} props.defaultExpanded - Default expanded state
 */
const FilterPanel = ({
  filters = [],
  values = {},
  onChange,
  onApply,
  onClear,
  collapsible = true,
  defaultExpanded = true
}) => {
  const [expanded, setExpanded] = useState(defaultExpanded);
  const [localValues, setLocalValues] = useState(values);

  const handleChange = (filterId, value) => {
    const newValues = { ...localValues, [filterId]: value };
    setLocalValues(newValues);
    if (onChange) {
      onChange(newValues);
    }
  };

  const handleApply = () => {
    if (onApply) {
      onApply(localValues);
    }
  };

  const handleClear = () => {
    const clearedValues = {};
    filters.forEach((filter) => {
      clearedValues[filter.id] = filter.defaultValue || '';
    });
    setLocalValues(clearedValues);
    if (onClear) {
      onClear();
    }
    if (onChange) {
      onChange(clearedValues);
    }
  };

  const renderFilter = (filter) => {
    const value = localValues[filter.id] || filter.defaultValue || '';

    switch (filter.type) {
      case 'text':
        return (
          <TextField
            fullWidth
            size="small"
            label={filter.label}
            value={value}
            onChange={(e) => handleChange(filter.id, e.target.value)}
            placeholder={filter.placeholder}
          />
        );

      case 'select':
        return (
          <FormControl fullWidth size="small">
            <InputLabel>{filter.label}</InputLabel>
            <Select
              value={value}
              label={filter.label}
              onChange={(e) => handleChange(filter.id, e.target.value)}
            >
              {filter.options?.map((option) => (
                <MenuItem key={option.value} value={option.value}>
                  {option.label}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        );

      case 'multiselect':
        return (
          <Autocomplete
            multiple
            size="small"
            options={filter.options || []}
            getOptionLabel={(option) => option.label}
            value={value || []}
            onChange={(e, newValue) => handleChange(filter.id, newValue)}
            renderInput={(params) => (
              <TextField {...params} label={filter.label} />
            )}
            renderTags={(value, getTagProps) =>
              value.map((option, index) => (
                <Chip
                  label={option.label}
                  size="small"
                  {...getTagProps({ index })}
                />
              ))
            }
          />
        );

      case 'date':
        return (
          <LocalizationProvider dateAdapter={AdapterDateFns}>
            <DatePicker
              label={filter.label}
              value={value || null}
              onChange={(newValue) => handleChange(filter.id, newValue)}
              renderInput={(params) => (
                <TextField {...params} fullWidth size="small" />
              )}
            />
          </LocalizationProvider>
        );

      case 'daterange':
        return (
          <LocalizationProvider dateAdapter={AdapterDateFns}>
            <Box sx={{ display: 'flex', gap: 1 }}>
              <DatePicker
                label={`${filter.label} From`}
                value={value?.from || null}
                onChange={(newValue) =>
                  handleChange(filter.id, { ...value, from: newValue })
                }
                renderInput={(params) => (
                  <TextField {...params} fullWidth size="small" />
                )}
              />
              <DatePicker
                label={`${filter.label} To`}
                value={value?.to || null}
                onChange={(newValue) =>
                  handleChange(filter.id, { ...value, to: newValue })
                }
                renderInput={(params) => (
                  <TextField {...params} fullWidth size="small" />
                )}
              />
            </Box>
          </LocalizationProvider>
        );

      case 'range':
        return (
          <Box>
            <Typography variant="caption" color="text.secondary" gutterBottom>
              {filter.label}
            </Typography>
            <Slider
              value={value || [filter.min || 0, filter.max || 100]}
              onChange={(e, newValue) => handleChange(filter.id, newValue)}
              valueLabelDisplay="auto"
              min={filter.min || 0}
              max={filter.max || 100}
              step={filter.step || 1}
              marks={filter.marks}
            />
            <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
              <Typography variant="caption">
                {value?.[0] || filter.min || 0}
              </Typography>
              <Typography variant="caption">
                {value?.[1] || filter.max || 100}
              </Typography>
            </Box>
          </Box>
        );

      case 'checkbox':
        return (
          <FormControlLabel
            control={
              <Checkbox
                checked={value || false}
                onChange={(e) => handleChange(filter.id, e.target.checked)}
              />
            }
            label={filter.label}
          />
        );

      case 'checkboxgroup':
        return (
          <Box>
            <Typography variant="caption" color="text.secondary" gutterBottom>
              {filter.label}
            </Typography>
            {filter.options?.map((option) => (
              <FormControlLabel
                key={option.value}
                control={
                  <Checkbox
                    checked={value?.includes(option.value) || false}
                    onChange={(e) => {
                      const currentValues = value || [];
                      const newValues = e.target.checked
                        ? [...currentValues, option.value]
                        : currentValues.filter((v) => v !== option.value);
                      handleChange(filter.id, newValues);
                    }}
                  />
                }
                label={option.label}
              />
            ))}
          </Box>
        );

      case 'radio':
        return (
          <FormControl component="fieldset">
            <Typography variant="caption" color="text.secondary" gutterBottom>
              {filter.label}
            </Typography>
            <RadioGroup
              value={value}
              onChange={(e) => handleChange(filter.id, e.target.value)}
            >
              {filter.options?.map((option) => (
                <FormControlLabel
                  key={option.value}
                  value={option.value}
                  control={<Radio />}
                  label={option.label}
                />
              ))}
            </RadioGroup>
          </FormControl>
        );

      default:
        return null;
    }
  };

  const activeFilterCount = Object.keys(localValues).filter(
    (key) => localValues[key] && localValues[key] !== ''
  ).length;

  return (
    <Paper sx={{ p: 2 }}>
      {/* Header */}
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          mb: expanded ? 2 : 0
        }}
      >
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <FilterIcon />
          <Typography variant="h6">Filters</Typography>
          {activeFilterCount > 0 && (
            <Chip
              label={activeFilterCount}
              size="small"
              color="primary"
              sx={{ ml: 1 }}
            />
          )}
        </Box>

        <Box sx={{ display: 'flex', gap: 1 }}>
          {activeFilterCount > 0 && (
            <Button
              size="small"
              startIcon={<ClearIcon />}
              onClick={handleClear}
            >
              Clear
            </Button>
          )}
          {collapsible && (
            <IconButton
              size="small"
              onClick={() => setExpanded(!expanded)}
            >
              {expanded ? <CollapseIcon /> : <ExpandIcon />}
            </IconButton>
          )}
        </Box>
      </Box>

      {/* Filters */}
      <Collapse in={expanded}>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          {filters.map((filter) => (
            <Box key={filter.id}>{renderFilter(filter)}</Box>
          ))}

          {/* Action Buttons */}
          {onApply && (
            <>
              <Divider sx={{ my: 1 }} />
              <Box sx={{ display: 'flex', gap: 1, justifyContent: 'flex-end' }}>
                <Button variant="outlined" onClick={handleClear}>
                  Clear All
                </Button>
                <Button variant="contained" onClick={handleApply}>
                  Apply Filters
                </Button>
              </Box>
            </>
          )}
        </Box>
      </Collapse>
    </Paper>
  );
};

export default FilterPanel;

// Made with Bob
