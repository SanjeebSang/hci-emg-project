import {Divider} from '@mui/material';
import './ui-container-section.css';


export default function UiContainerSection(props) {

    let classNames = "";
    if (props.classes) {
        classNames += props.classes;
    }

    return (
    <div className='ui-container-section-root'>
        <div className={classNames}>
            {props.children}
        </div>
        <div className='ui-container-section-divider'><Divider /></div>
    </div>
    );
}