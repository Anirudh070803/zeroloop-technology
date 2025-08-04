import React from 'react';
import { Paper, Typography, Box, Chip } from '@mui/material';

const DynamicReport = ({ data }) => {
  return (
    <Paper variant="outlined" sx={{ p: 2, mt: 2 }}>
      <Typography variant="h6" gutterBottom>Dynamic Analysis Report (Echidna)</Typography>
      {data.bug_found ? (
        <Chip label="Vulnerability Found!" color="error" sx={{ mb: 2 }} />
      ) : (
        <Chip label="No Vulnerabilities Found" color="success" sx={{ mb: 2 }} />
      )}
      <Typography variant="subtitle2" sx={{ fontWeight: 'bold' }}>Full Log:</Typography>
      <Paper variant="outlined" sx={{ p: 2, whiteSpace: 'pre-wrap', fontFamily: 'monospace', maxHeight: 200, overflow: 'auto', backgroundColor: '#222' }}>
        {data.output}
      </Paper>
    </Paper>
  );
};

export default DynamicReport;