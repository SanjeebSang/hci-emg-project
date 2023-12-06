import React from 'react'
import { Typography, Tooltip } from '@mui/material';
import Button from "@mui/material/Button"
import {Link} from 'react-router-dom'
import UiContainer from './ui-container';
import UnityButton from '../generics/unity-button';
import ImpText from './imp-text';


export default function ExperimentHasEnded(props) {

	return (
	<UiContainer>
		<Typography variant='h3'>End of VR EMG Experiment</Typography>
		<ul>
			<TypographyParagraph text='Thank you for participating in this experiment where you performed EMG hand movements as shown in this VR space.' />
			<TypographyParagraph text='Please take some time to fill out a survey to let us know more about this experiment.' />
			<TypographyParagraph text='You can now remove your headset. Let us know if you encountered any issues.' />
		</ul>
		<Typography variant='body1'>In case you want to view the experiment screen again, you can click on the <ImpText>View the Experiment Start Screen</ImpText> button to go back to the experiment start.</Typography>
		<div style={{paddingTop: "32px"}}>
		<Link to='/start'>
			
          <UnityButton>View the Experiment Start Screen</UnityButton>
         
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