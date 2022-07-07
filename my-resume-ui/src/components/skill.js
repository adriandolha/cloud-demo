import Typography from '@material-ui/core/Typography';
import resumeTheme from '../theme';
import { useTheme, createStyles, makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) =>
    createStyles({

        skill: {
            borderRadius: '10px',
            backgroundColor: theme.palette.primary.main,
            // padding: theme.spacing(0.4),
            // margin: theme.spacing(0.2),
            padding: '1px 10px 1px 10px',
            margin: '3px 3px 3px 3px',


            color: 'white'
        }


    }),
);

const useStyless = makeStyles({
    skill: {
        borderRadius: '10px',
        backgroundColor: props=> props.color,
        // padding: theme.spacing(0.4),
        // margin: theme.spacing(0.2),
        padding: '1px 10px 1px 10px',
        margin: '3px 3px 3px 3px',


        color: 'white'
    }
});

function Skill({ skill, color }) {
    const theme = resumeTheme(useTheme());
    const classes = useStyles(theme);
    const skillVariant = 'body1'
    return (
        <Typography variant={skillVariant} className={classes.skill}>{skill}</Typography>
    );
}

export default Skill;
