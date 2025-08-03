import React from 'react';
import { Box, Typography, Container } from '@mui/material';

const Footer = () => {
  return (
    <Box component="footer" sx={{ bgcolor: 'background.paper', py: 6, mt: 'auto' }}>
      <Container maxWidth="lg">
        <Typography variant="body2" color="text.secondary" align="center">
          {'© '}
          {new Date().getFullYear()}
          {' ZeroLoop Technology. All rights reserved.'}
        </Typography>
      </Container>
    </Box>
  );
};
export default Footer;