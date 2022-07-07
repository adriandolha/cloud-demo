import resumeTheme from '../theme';
import { useTheme } from '@material-ui/core/styles';



function Marker_({ name, bounds, color }) {
    const theme = resumeTheme(useTheme());
    // console.log('marker')
    // console.log(name)
    // console.log(bounds)

    return (
        <div style={{
            display: 'block',
            position: 'absolute',
            // position: 'relative',
            top: bounds.top,
            bottom: bounds.bottom,
            // bottom: props => props.bounds.bottom,
            width: '60px',
            height: bounds.height,
            // minHeight: props => props.bounds.height,
            backgroundColor: color
        }}></div>

    );
}

function Marker({ name, bounds, color }) {
    const theme = resumeTheme(useTheme());

    return (
        <div style={{
            maxWidth: '60%',
            minWidth: '60%',
            minHeight: '100%',
            backgroundColor: color
        }}></div>

    );
}

export default Marker;
