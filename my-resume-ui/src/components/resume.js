import { Divider } from '@material-ui/core';
import resumeTheme from '../theme';
import { useTheme, createStyles, makeStyles, ThemeProvider } from '@material-ui/core/styles';
import PersonalDetails from './personal-details';
import ResumeBody from './resume-body';
import resume from '../resume-data.js'

const useStyles = makeStyles((theme) =>
    createStyles({
        mainTitle: {
            backgroundColor: theme.palette.primary.main,
            margin: '10px 0 30px 0',
            paddingBottom: '10px',
            borderRadius: '10px'
        },
        resume: {
            border: '2px solid black',
            padding: '20px 40px 20px 40px',
            margin: '10px 20px 100px 20px'
        },
        divider: {
            color: theme.palette.primary.main,
            backgroundColor: theme.palette.primary.main,
            height: '3px'

        }
    }),
);

function Resume() {
    const classes = useStyles(resumeTheme(useTheme()));
    console.log(resume)
    return (
        <div className={`{classes.resume} resume`}>
            <PersonalDetails />
            <Divider orientation='horizontal' className={classes.divider} />
            <ResumeBody resume={resume} />
        </div>
    );
}

export default Resume;