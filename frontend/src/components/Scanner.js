import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Paper, Typography, Button, Box, CircularProgress, Alert } from '@mui/material';
import { v4 as uuidv4 } from 'uuid';
import StaticReport from './StaticReport';
import DynamicReport from './DynamicReport';

const Scanner = () => {
    const [contractFile, setContractFile] = useState(null);
    const [testFile, setTestFile] = useState(null);
    const [isScanning, setIsScanning] = useState(false);
    const [results, setResults] = useState([]);
    const [clientId] = useState(uuidv4());

    useEffect(() => {
        const ws = new WebSocket(`ws://localhost:8000/ws/${clientId}`);
        ws.onmessage = (event) => {
            const resultData = JSON.parse(event.data);
            setResults(prevResults => [...prevResults, resultData]);
        };
        ws.onclose = () => {
            setIsScanning(false); // Stop scanning indicator when connection closes
        };
        return () => {
            ws.close();
        };
    }, [clientId]);

    const handleSubmit = async () => {
        if (!contractFile || !testFile) return;
        setIsScanning(true);
        setResults([]);
        const formData = new FormData();
        formData.append('client_id', clientId);
        formData.append('contract_file', contractFile);
        formData.append('test_file', testFile);
        try {
            await axios.post('http://localhost:8000/scan/file', formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
            });
        } catch (error) {
            console.error("Failed to start scan:", error);
            setResults([{ error: `Failed to start scan: ${error.message}` }]);
            setIsScanning(false);
        }
    };

    return (
        <Paper elevation={3} sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom>
                Smart Contract Scanner
            </Typography>
            <Typography paragraph color="text.secondary">
                Upload your smart contract and test files to begin the automated security audit.
            </Typography>

            <Box sx={{ mt: 3, display: 'flex', alignItems: 'center', gap: 2 }}>
                <Button variant="outlined" component="label">
                    Contract File (.sol)
                    <input type="file" hidden accept=".sol" onChange={(e) => setContractFile(e.target.files[0])} />
                </Button>
                {contractFile && <Typography variant="caption">{contractFile.name}</Typography>}
                <Button variant="outlined" component="label">
                    Test File (.sol)
                    <input type="file" hidden accept=".sol" onChange={(e) => setTestFile(e.target.files[0])} />
                </Button>
                {testFile && <Typography variant="caption">{testFile.name}</Typography>}
            </Box>
            
            <Box sx={{ mt: 2 }}>
                 <Button variant="contained" onClick={handleSubmit} disabled={!contractFile || !testFile || isScanning}>
                    Start Scan
                </Button>
            </Box>

            {isScanning && (
                <Box sx={{ mt: 3, display: 'flex', alignItems: 'center', gap: 2 }}>
                    <CircularProgress size={24} />
                    <Typography>Scan in progress... Results will appear here in real-time.</Typography>
                </Box>
            )}

            {results.length > 0 && (
                <Box sx={{ mt: 4 }}>
                    <Typography variant="h6" gutterBottom>Scan Results:</Typography>
                    {results.map((result, index) => (
                        <Box key={index} sx={{my: 2}}>
                            {result.error ? (
                                <Alert severity="error">{result.error}</Alert>
                            ) : result.scan_type === 'static_analysis' ? (
                                <StaticReport data={result.data} />
                            ) : result.scan_type === 'dynamic_analysis' ? (
                                <DynamicReport data={result.data} />
                            ) : null}
                        </Box>
                    ))}
                </Box>
            )}
        </Paper>
    );
};

export default Scanner;