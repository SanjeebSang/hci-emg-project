import './experiment-ui.css';
import LinearWithValueLabel from './linear-progress';
import React from 'react';
import Logo from './logo.svg';
import { Typography, Tooltip } from '@mui/material';
import UiContainer from './ui-container';
import UiContainerSection from './ui-container-section';
import UnityButton from '../generics/unity-button';
import CircularWithValueLabel from './circular-progress';
import ImpText from './imp-text';
import HandClose from './images/Hand_Close.png';
import HandOpen from './images/Hand_Open.png';
import NoMotion from './images/No_Motion.png';
import WristExtension from './images/Wrist_Extension.png';
import WristFlexion from './images/Wrist_Flexion.png';
import Ready from './images/ready.jpg';
import ExperimentMovementNotifier from '../common/action-notifier';

const DESCRIPTIONS = ['Hand Close', 'Hand Open', 'No Motion', 'Wrist Extension', 'Wrist Flexion'];
const IMAGES = [HandClose, HandOpen, NoMotion, WristExtension, WristFlexion];

export default class ExperimentUI extends React.Component {

  intervalLength = 500;
  intervalLengthFromEnv = process.env.REACT_APP_INTERVAL_LENGTH;

  constructor(props) {
    super(props);
    this.state = this.getInitialState();

    this.changeStateAfterInterval = this.changeStateAfterInterval.bind(this);
    this.startTimer = this.startTimer.bind(this);
    this.nextRep = this.nextRep.bind(this);
    this.redoRep = this.redoRep.bind(this);
    this.actionNotifier = new ExperimentMovementNotifier();
    this.actionNotifier.notifyExperimentHasStarted(Date.now());
  }

  getInitialState() {
    return {
      rep: 1,
      epn: 1,
      progress: 0,
      startRep: true,
      completed: false,
      showPreview: true,
      previewTime: 0,
      current: 0,
      selected: [] 
    };
  }
  
  startTimer() {
    let timerIntervalInMilis = this.intervalLength;
    this.timer = setInterval(() => 
      this.setState((ps) => this.changeStateAfterInterval(ps)),
      timerIntervalInMilis
    );
  }

  changeStateAfterInterval(ps) {
    if (ps.completed || ps.startRep == false) {
      return ps;
    }

    // All the states
    let progress = ps.progress;
    let rep = ps.rep;
    let startRep = ps.startRep;
    let epn = ps.epn;
    let completed = ps.completed;
    let showPreview = ps.showPreview;
    let previewTime = ps.previewTime;
    let current = ps.current;
    let selected = ps.selected;

    if (showPreview) {
      previewTime = previewTime + 10;

      if (previewTime == 50) {
        let timeInMillis = Date.now() + (this.intervalLength * 3);
        this.actionNotifier.notify(rep, current, timeInMillis); 
      }

      if (previewTime > 50) {
        showPreview = false;
        previewTime = 0;
      }

      return {previewTime, showPreview};
    } 

    // Start changing states
    progress = ps.progress + 10;
    if (progress > 100) {
      // completed.push("${rep}-${epn}");
      epn = epn + 1; 
      showPreview = true;
      progress = 0;
      if (epn > 5) {
        rep = rep + 1;
        epn = 1;
        startRep = false;
        selected = [];
      }
      else {
        selected.push(current);
      }

      current = this.getNewExperimentNumber(selected);
      if (rep > 5) {
        completed = true;
        this.actionNotifier.notifyExperimentHasEnded(Date.now());
      }
    }

    return {progress, epn, rep, completed, startRep, showPreview, current, selected};
  }

  getNewExperimentNumber(selected) {
    // console.log("Selected");
    // console.log(selected);
    let available = [];
    for (let i = 0; i < 5; i++) {
      if (!selected.includes(i)) {
          available.push(i);
      }
    }

    // console.log("Available");
    // console.log(available);

    if (available.length == 1) return available[0];
    let randomIndex = Math.floor(Math.random() * available.length);
    // console.log("Random Index");
    // console.log(available[randomIndex]);
    return available[randomIndex];
  }

  componentDidMount() {
    this.startTimer();
  }

  nextRep() {
    this.setState({startRep: true});
  }

  redoRep() {
    this.setState((ps) => {
      return {rep: (ps.rep - 1), startRep: true};
    });
  }

  render() {

    return(
      <UiContainer>
      <DescritpionSection ms={this.state} />
      <ImageSection ms={this.state} />
      <PreviewSection ms={this.state} il={this.intervalLength} />
      <ProgressSection ms={this.state} />
      <InteractionSection onRedo={this.redoRep} 
        onNext={this.nextRep} ms={this.state} />
    </UiContainer>
    );
  }

}


function DescritpionSection(props) {

  let progress = props.ms.progress;
  let epn = props.ms.epn;
  let rep = props.ms.rep;
  let epnProgress = (epn - 1) * 20 + (progress / 100 * 20);
  let repProgress = (rep - 1) * 20 + (epn - 1) * 4;

  if (props.ms.startRep == false) {

    
  progress = 0;
  epn = 1;
  rep = props.ms.rep;
  epnProgress = (epn - 1) * 20 + (progress / 100 * 20);
  repProgress = (rep - 1) * 20 + (epn - 1) * 4;
    
    return(
      <UiContainerSection classes='eui-section-1'>
        <div className='flex-columns'>
        <Typography style={{marginRight: '16px'}} variant='h6' color=''>Next Rep to start: {props.ms.rep}</Typography>
        <div style={{flexGrow: 1}}></div>
        <Typography variant='body2'>Reps Completed: </Typography>
        <CircularWithValueLabel progress={repProgress} />
        </div>
      </UiContainerSection>);
  }

  let description = DESCRIPTIONS[props.ms.current];

    return(
    <UiContainerSection classes='eui-section-1'>
      <div className='flex-columns'>
      <Typography style={{marginRight: '16px'}} variant='h6' color=''>Current Rep: {props.ms.rep}</Typography>
      <div style={{flexGrow: 1}}></div>
      <Typography variant="body2">Rep Progress: </Typography>
      <CircularWithValueLabel progress={repProgress} />
      </div>
      <div className='flex-columns'>
      <Typography  style={{marginRight: '16px'}} variant='body1' color=''>Movement: {props.ms.current}. {description}</Typography>
      <div style={{flexGrow: 1}}></div>
      <Typography variant="body2">Movement Progress: </Typography>
      <CircularWithValueLabel progress={epnProgress} />
      </div>
   
    
    </UiContainerSection>);
}


function ImageSection(props) {

  let image = IMAGES[props.ms.current];
  let imgStyles={'opacity': 1};

  if (props.ms.startRep == false) 
  {
      image = Ready;
  }

  if (props.ms.showPreview && props.ms.startRep) {
    imgStyles['opacity'] = 0;
  }

    return(
    <UiContainerSection classes='eui-section-1'>
      <div className='center-image-container'>
        <img className='exp-ui-image' src={image} style={imgStyles} alt="" />
      </div>

    </UiContainerSection>);
}

// function ProgressSection(props) {

//   const [progress, setProgress] = React.useState(0);

//   React.useEffect(() => {
//     const timer = setInterval(() => {
//       setProgress((prevProgress) => (prevProgress >= 100 ? 100 : prevProgress + 10));
//     }, 500);
//     return () => {
//       clearInterval(timer);
//     };
//   }, []);

//     return(
//     <div className='eui-section-1'>
//       <LinearWithValueLabel progress={progress} />

//     </div>);
// }


function PreviewSection(props) {

  if (props.ms.showPreview && props.ms.startRep) {
    let repNum = props.ms.rep;
    let preview = props.ms.previewTime;
    let totalTime = props.il * 5;
    let timeRemainingInSeconds = ((50 - preview)/10).toFixed(0); 
  
      return(
      <UiContainerSection classes='eui-section-1' style={{color: 'black', backgroundColor: "black"}}>
        <div style={{paddingLeft: '8px'}}>
        {/* <Typography variant='body2' color=''>This is only a preview, not an experiment. This preview allows you to view the movement info before your experiment starts.</Typography> */}
        <Typography variant='body1' color=''>Next movement (#{props.ms.epn}) starts in: {timeRemainingInSeconds}</Typography>
        </div>
        <div>
          <LinearWithValueLabel progress={preview * 2} />
        </div>
      </UiContainerSection>);
  }
else {

      return(<div></div>);
  
}

}

function ProgressSection(props) {
  if (!props.ms.showPreview) {
  if (props.ms.startRep) {

  let cs = props.ms.progress / 20;
  let rs = 5 - cs;
  rs = rs.toFixed(1);

  return(
    <UiContainerSection classes='eui-section-1'>
      <div style={{paddingLeft: '8px'}}>
        <Typography variant='title' color='primary'>Perform the specified movement.</Typography>
      </div>
      <LinearWithValueLabel progress={props.ms.progress} />
      <div style={{paddingLeft: '8px'}}>
        <Typography variant='body1'>Time Remaining: {rs} seconds.</Typography>
      </div>
    </UiContainerSection>);
  }
  else {
    return (<div></div>);
  }
}
else {
  return (<div></div>);
}
}

function InteractionSection(props) {

  let html = [];
  if (props.ms.startRep == false) {
    html.push(<Typography key="int-sec-1" color='secondary' variant='h6'>Action Needed!</Typography>);
    html.push(<Typography key="int-sec-2" variant='body2'>Click on the  
    <ImpText> Start Next Repetition</ImpText> 
    to move on to the next repetition. Or, if you need you need to redo this 
    section, click on the <ImpText>Redo Current Repetition</ImpText> to redo this repetition.</Typography>);

  

  let handleNext = () => {
    props.onNext();
  };

  let handleRedo = () => {
    props.onRedo();
  };

    return(
      <UiContainerSection>
        <div style={{marginBottom: '24px'}}>{html}</div>
        <div className='flex-columns-reverse'>
        <div className='flex-childr' style={{marginRight: '16px'}}>
        <UnityButton onClick={handleNext}>Start Repetition {props.ms.rep}</UnityButton>

        </div>
        <div className='flex-childr' style={{marginRight: '16px'}}>
        <UnityButton onClick={handleRedo}>Redo Repetition {props.ms.rep - 1}</UnityButton>

        </div>
       
        </div>
        
      </UiContainerSection>);
  }
  else {
    return (<div></div>);
  }

}


