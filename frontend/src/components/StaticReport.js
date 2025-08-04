import React from 'react';
import { Paper, Typography, Box, Chip, Divider } from '@mui/material';

const StaticReport = ({ data }) => {
  return (
    <Paper variant="outlined" sx={{ p: 2 }}>
      <Typography variant="h6" gutterBottom>Static Analysis Report (Slither + AI)</Typography>
      <Typography variant="body1" sx={{ mb: 2 }}>{data.summary}</Typography>
      <Divider sx={{ mb: 2 }} />
      {data.vulnerabilities.length > 0 ? (
        data.vulnerabilities.map((vuln, index) => (
          <Box key={index} sx={{ mb: 2 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
              <Typography variant="subtitle1" sx={{ fontWeight: 'bold' }}>{vuln.name}</Typography>
              <Chip label={vuln.severity} color={vuln.severity === 'High' ? 'error' : 'warning'} size="small" />
              <Chip label={`Confidence: ${vuln.confidence}`} color="info" size="small" variant="outlined" />
            </Box>
            <Typography variant="body2" sx={{ fontStyle: 'italic', color: 'text.secondary', mb: 1 }}>
              {vuln.simplified_explanation}
            </Typography>
          </Box>
        ))
      ) : (
        <Typography>No vulnerabilities found.</Typography>
      )}
    </Paper>
  );
};

export default StaticReport;