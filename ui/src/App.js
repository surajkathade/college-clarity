import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Box, Container, TextField, MenuItem, Select, OutlinedInput, Chip, Checkbox, Autocomplete, Button, Table, TableBody, TableCell, TableHead, TableRow, Paper, FormControl, FormLabel, ListItemText } from '@mui/material';
import backgroundImage from './background_image_2.jpeg';

function App() {
  const [airmain, setAirmain] = useState('');
  const [airadvanced, setAiradvanced] = useState('');
  const [selectedBranches, setSelectedBranches] = useState([]);
  const [selectedSeattype, setSelectedSeattype] = useState('');
  const [selectedStates, setSelectedStates] = useState('');
  const [selectedGender, setSelectedGender] = useState('');
  const [branches, setBranches] = useState([]);
  const [seattype, setSeatType] = useState([]);
  const [states, setStates] = useState([]);
  const [gender, setGender] = useState(['Male', 'Female']);
  const [tableData, setTableData] = useState([]);

  // Fetch options for the multiselect dropdown
  useEffect(() => {
    getBranches();
    getSeattype();
    getStates();
  }, []);

  const getBranches = async () => {
    const resp = await axios.get('http://localhost:5000/branches');
    setBranches(resp.data);
  }

  const getSeattype = async () => {
    const resp = await axios.get('http://localhost:5000/seattypes');
    setSeatType(resp.data);
  }

  const getStates = async () => {
    const resp = await axios.get('http://localhost:5000/states');
    setStates(resp.data);
  }

  const handleAirmainChange = (event) => {
    setAirmain(event.target.value);
  };

  const handleAiradvancedChange = (event) => {
    setAiradvanced(event.target.value);
  };

  const handleBranchChange = (event, value) => {
    setSelectedBranches(value);
  };

  const handleSeattypeChange= (event, value) => {
    setSelectedSeattype(value);
  };

  const handleStateChange = (event, value) => {
    setSelectedStates(value);
  };

  const handleGenderChange = (event, value) => {
    setSelectedGender(value);
  };

  const handleSubmit = async() => {
    try {
      const reqBody = {
        'air_main': airmain,
        'air_advanced': airadvanced,
        'branches': selectedBranches,
        'seattype': selectedSeattype,
        'state': selectedStates,
        'gender': selectedGender
      }
      const result = await axios.post('http://localhost:5000/list', reqBody);
      setTableData(result.data);
    } catch (error) {
      console.error('Error posting data:', error);
    }
  };

  // Inline CSS for the background image
  const containerStyle = {
    position: 'relative',
    minHeight: '100vh',
    padding: '20px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  };

  const backgroundStyle = {
    position: 'absolute',
    top: 0,
    left: 0,
    width: '100%',
    height: '100%',
    backgroundImage: `url(${backgroundImage})`,
    backgroundSize: 'cover',
    backgroundPosition: 'center',
    backgroundRepeat: 'no-repeat',
    opacity: 0.2, // Adjust this value to control the fade effect
    zIndex: -1, // Ensure the background stays behind the content
  };

  const paperStyle = {
    marginTop: '20px',
    padding: '20px',
    // backgroundColor: 'rgba(255, 255, 255, 0.8)', // Slightly opaque white background
    // backdropFilter: 'blur(10px)', // Optional: adds a blur effect behind the table
    backgroundColor: 'transparent',
  };

  const tableStyle = {
    backgroundColor: 'transparent',
    boxShadow: 'none', // Optional: removes shadow if present
  };

  return (
    <div style={containerStyle}>
      <div style={backgroundStyle}></div>
      <Container style={{ zIndex: 1 }}>
        <h1>Welcome to College Clarity</h1>
        <h3>Sneak peek into your dream colleges</h3>
        <Box display="flex" justifyContent="space-between" gap={2}>
        <FormControl fullWidth margin="normal">
          <FormLabel style={{ fontWeight: 'bold' }}>Please Select Category</FormLabel>
          <Autocomplete
            // multiple
            options={seattype}
            disableCloseOnSelect
            onChange={handleSeattypeChange}
            renderInput={(params) => (
              <TextField
                {...params}
                variant="outlined"
                // label="Select Options"
                placeholder="Start typing to search"
              />
            )}
            renderOption={(props, option, { selected }) => (
              <MenuItem
                component="li"
                {...props}
              >
                <ListItemText primary={option} />
              </MenuItem>
            )}
          />
        </FormControl>
        <FormControl fullWidth margin="normal">
          <FormLabel style={{ fontWeight: 'bold' }}>Please Select Gender</FormLabel>
          <Autocomplete
            // multiple
            options={gender}
            disableCloseOnSelect
            onChange={handleGenderChange}
            renderInput={(params) => (
              <TextField
                {...params}
                variant="outlined"
                // label="Select Options"
                placeholder="Start typing to search"
              />
            )}
            renderOption={(props, option, { selected }) => (
              <MenuItem
                component="li"
                {...props}
              >
                <ListItemText primary={option} />
              </MenuItem>
            )}
          />
        </FormControl>
        <FormControl fullWidth margin="normal">
          <FormLabel style={{ fontWeight: 'bold' }}>Please Select Home State</FormLabel>
          <Autocomplete
            // multiple
            options={states}
            disableCloseOnSelect
            onChange={handleStateChange}
            renderInput={(params) => (
              <TextField
                {...params}
                variant="outlined"
                // label="Select Options"
                placeholder="Start typing to search"
              />
            )}
            renderOption={(props, option, { selected }) => (
              <MenuItem
                component="li"
                {...props}
              >
                {/* <Checkbox
                  checked={selected}
                  style={{ marginRight: 8 }}
                /> */}
                <ListItemText primary={option} />
              </MenuItem>
            )}
          />
        </FormControl>
        </Box>
        <Box display="flex" justifyContent="space-between" gap={2}>
        {/* Integer Input with Label */}
        <FormControl fullWidth margin="normal">
          <FormLabel style={{ fontWeight: 'bold' }}>AIR Main</FormLabel>
          <TextField
            type="number"
            value={airmain}
            onChange={handleAirmainChange}
            variant="outlined"
          />
        </FormControl>
        <FormControl fullWidth margin="normal">
          <FormLabel style={{ fontWeight: 'bold' }}>AIR Advanced</FormLabel>
          <TextField
            type="number"
            value={airadvanced}
            onChange={handleAiradvancedChange}
            variant="outlined"
          />
        </FormControl>
        <FormControl fullWidth margin="normal">
          <FormLabel>AIR Paper II (A)</FormLabel>
          <TextField
            disabled
            // type="number"
            // value={integerValue}
            // onChange={handleIntegerChange}
            variant="outlined"
            // sx={{
            //   "& .Mui-disabled": {
            //     backgroundColor: "#f5f5f5", // Customize the disabled background color
            //   },
            // }}
          />
        </FormControl>
        <FormControl fullWidth margin="normal">
          <FormLabel>AIR Paper II (B)</FormLabel>
          <TextField
            disabled
            // type="number"
            // value={integerValue}
            // onChange={handleIntegerChange}
            variant="outlined"
            // sx={{
            //   "& .Mui-disabled": {
            //     backgroundColor: "#f5f5f5", // Customize the disabled background color
            //   },
            // }}
          />
        </FormControl>
        </Box>
        
        {/* Multiselect Dropdown with Label */}
        <FormControl fullWidth margin="normal">
          <FormLabel style={{ fontWeight: 'bold' }}>Please Select Academic Program preferences</FormLabel>
          {/* <Select
            multiple
            value={selectedOptions}
            onChange={handleOptionChange}
            input={<OutlinedInput />}
            renderValue={(selected) => (
              <div>
                {selected.map((value) => (
                  <Chip key={value} label={value} />
                ))}
              </div>
            )}
            variant="outlined"
          >
            {options.map((option) => (
              <MenuItem key={option} value={option}>
                <Checkbox checked={selectedOptions.indexOf(option) > -1} />
                {option}
              </MenuItem>
            ))}
          </Select> */}
          {/* <Autocomplete
            multiple
            options={options}
            onChange={handleOptionChange}
            renderInput={(params) => (
              <TextField
                {...params}
                variant="outlined"
                label="Select Options"
                placeholder="Start typing to search"
              />
            )}
            renderTags={(value, getTagProps) =>
              value.map((option, index) => (
                <Chip label={option} {...getTagProps({ index })} key={index} />
              ))
            }
            filterSelectedOptions
          /> */}
          <Autocomplete
            multiple
            options={branches}
            disableCloseOnSelect
            onChange={handleBranchChange}
            renderInput={(params) => (
              <TextField
                {...params}
                variant="outlined"
                // label="Select Options"
                placeholder="Start typing to search"
              />
            )}
            renderOption={(props, option, { selected }) => (
              <MenuItem
                component="li"
                {...props}
              >
                <Checkbox
                  checked={selected}
                  style={{ marginRight: 8 }}
                />
                <ListItemText primary={option} />
              </MenuItem>
            )}
          />
        </FormControl>

        <Button
          variant="contained"
          color="primary"
          onClick={handleSubmit}
          style={{ marginTop: '20px' }}
        >
          Get College list
        </Button>

        {/* Table */}
        {tableData.length > 0 && (
          <Paper style={paperStyle}>
            <Table style={tableStyle}>
              <TableHead>
                <TableRow>
                  <TableCell>College Rank</TableCell>
                  <TableCell>College Name</TableCell>
                  <TableCell>Academic Program Name</TableCell>
                  <TableCell>Opening Rank</TableCell>
                  <TableCell>Closing Rank</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {tableData.map((row, index) => (
                  <TableRow key={index}>
                    <TableCell>{row['Rank']}</TableCell>
                    <TableCell>{row['Institute']}</TableCell>
                    <TableCell>{row['Academic Program Name']}</TableCell>
                    <TableCell>{row['Opening Rank']}</TableCell>
                    <TableCell>{row['Closing Rank']}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </Paper>
        )}
      </Container>
    </div>
  );
}

export default App;
