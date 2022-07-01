import Typography from '@material-ui/core/Typography';
import resumeTheme from '../theme';
import { useTheme, createStyles, makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) =>
    createStyles({

        skill: {
            borderRadius: '10px',
            backgroundColor: theme.palette.primary.main,
            // float: 'left',
            padding: '3px 10px 3px 10px',
            margin: '3px 5px 3px 5px',
            color: 'white'
        }


    }),
);

function Skill({skill}) {
    const theme = resumeTheme(useTheme());
    const classes = useStyles(theme);
    const skillVariant = 'h6'
    return (
        <Typography variant={skillVariant} className={classes.skill}>{skill}</Typography>
    );
}

export default Skill;
