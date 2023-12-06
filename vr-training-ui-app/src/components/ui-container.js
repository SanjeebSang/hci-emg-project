import './ui-container.css';

export default function UiContainer (props) {

    return (
    <div className='ui-container-root'>
        <div className='ui-container-l2'>
            {props.children}
        </div>
    </div>
    
    );
}