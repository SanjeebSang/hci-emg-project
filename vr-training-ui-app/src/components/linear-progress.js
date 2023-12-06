import * as React from 'react';
import LinearProgress, { LinearProgressProps } from '@mui/material/LinearProgress';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

function LinearProgressWithLabel(props) {
  return (
    <Box>
      <Box sx={{ width: '100%-32px', mr: 1, padding: "8px" }}>
        <LinearProgress variant="determinate" {...props} />
      </Box>
      <div style={{padding: "8px"}}>
        <Typography variant="body1" color="text.primary">{`${Math.round(
          props.value,
        )}%`}</Typography>
      </div>
    </Box>
  );
}

export default function LinearWithValueLabel(props) {

  return (
    <Box sx={{ width: '100%' }}>
      <LinearProgressWithLabel value={props.progress} />
    </Box>
  );
}