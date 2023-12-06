import React from 'react'
import { Typography, Tooltip } from '@mui/material';
import Button from "@mui/material/Button"
import {Link} from 'react-router-dom'
import UiContainer from './ui-container';
import UnityButton from '../generics/unity-button';
import ImpText from './imp-text';

export default function ExperimentWillStart(props) {

	return (
	<UiContainer>
		<Typography variant='h3'>Welcome to VR EMG Experiment</Typography>
		<ul>
			<TypographyParagraph text='In this experiment you will perform EMG hand movements as shown in this VR space.' />
			<TypographyParagraph text='You will need to move your hands for 5 seconds for each hand movement shown in display.' />
			<TypographyParagraph text='You will need 5 different movements for 5 reps. You can stop and redo the experiment at any instance.' />
		</ul>
		<Typography variant='body1'>Click the <ImpText>Start the Experiment</ImpText> button to start the experiment</Typography>
		<div style={{paddingTop: "16px", paddingBottom: "16px"}}>
		<Link to='/experiment'>
			
			<UnityButton>Start the Experiment</UnityButton>
		   
			  </Link>
		</div>

		<Typography variant='body1'>Click the <ImpText>Audit the Experiment</ImpText> to audit/view the experiment. This will allow you to view the experiment without loading any data. 
		Use this option in case you just want to review the experiment. </Typography>
		<div style={{paddingTop: "16px"}}>
		<Link to='/experiment'>
			
          <UnityButton>Audit the Experiment</UnityButton>
         
			</Link>
		</div>
	</UiContainer>);
}

function TypographyParagraph(props) {

	return (
		<li>
			<Typography variant='body1'>
				{props.text}
			</Typography>
		</li>
	);
}