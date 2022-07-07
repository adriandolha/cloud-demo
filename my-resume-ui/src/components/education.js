import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import { List, ListItem } from '@material-ui/core';
import resumeTheme from '../theme';
import { useTheme, createStyles, makeStyles } from '@material-ui/core/styles';
import MarkedComponent from './marked-component';
const useStyles = makeStyles((theme) =>
    createStyles({
        education: {
            marginRight: theme.spacing(2)
        },
        sectionTitle: {
            float: 'left',
            fontWeight: 'bold'
        },
        educationSpecialization: {
            float: 'left',
            fontWeight: 'bold'
        },
        educationTitle: {
            float: 'left'
        },
        educationDate: {
            fontStyle: 'italic',
            // float: 'left',
            color: theme.palette.success.main,
        },
        educationLocation: {
            fontStyle: 'italic',
            // float: 'left',
            color: theme.palette.success.main,
        },
    }),
);

function Education({ data }) {
    const theme = resumeTheme(useTheme());
    const classes = useStyles(theme);
    const Header = () => (
        <Grid item container direction='column'>
            <Grid item>
                <Typography variant="h6" className={classes.educationSpecialization}>
                    {data.specialization}
                </Typography>
            </Grid>
            <Grid item>
                <Typography variant="h5" className={classes.educationTitle}>
                    {data.title}
                </Typography>
            </Grid>
        </Grid>
    )
    const EducationDetails = () => (
        <Grid item container justifyContent='space-between'>
            <Typography variant="body1" align='left' className={classes.educationDate}>
                {data.from} - {data.to}
            </Typography>
            <Typography variant="body1" align='left' className={classes.educationLocation}>
                {data.location}
            </Typography>
        </Grid>
    )
    return (
        <Grid item container xs={12} md={12} lg={12} direction='column' className={classes.education}>
            <MarkedComponent component={<Header />} markerColor={theme.palette.success.main} />
            <MarkedComponent component={<EducationDetails />}/>
        </Grid>
    );
}

export default Education;
