import resumeTheme from '../theme';
import { Box, Typography } from '@material-ui/core';
import { useTheme, createStyles, makeStyles } from '@material-ui/core/styles';
import Marker from './marker';
import Grid from '@material-ui/core/Grid';
const useStyles = makeStyles((theme) =>
    createStyles({
        markerCol: {
            flexBasis: '60px',
            minWidth: '60px',
            // miaxWidth: '100px',
            // minHeight: '100px'
        },
        markerContainer: {

        }


    }),
);


function MarkedComponent({ component, markerColor }) {
    const theme = resumeTheme(useTheme());
    const classes = useStyles(theme);

    return (
        <Grid container  className='markedContainer' wrap="nowrap">
            <Grid item className={classes.markerCol}>
                {markerColor && <Marker color={markerColor} />}
            </Grid>
            <Grid item xs="auto" md="auto" lg="auto">
                {component}
            </Grid>
        </Grid >

    );
}

export default MarkedComponent;
